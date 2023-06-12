#!/usr/bin/env python3
"""
Multiprocess asyncio consumer runner 
"""

import asyncio
import concurrent.futures
import multiprocessing
import os
from queue import Empty


work_queue = multiprocessing.Manager().Queue()
result_queue = multiprocessing.Manager().Queue()


async def async_coro_runner(coro):
    """
    Run the passed coro with arg popped from work_queue until queue is empty then finish and exit
    """
    background_tasks = set()
    while True:
        try:
            arg = work_queue.get_nowait()
        except Empty:
            await asyncio.gather(*background_tasks)
            break
        task = asyncio.create_task(coro(arg))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)


def forked_process(coro):
    """
    Minimal entrypoint to async queue worker
    """
    asyncio.run(async_coro_runner(coro))


def task_runner(coro, num_children: int = None):
    """
    Run a coro across multiple processes
    """
    num_children = num_children or os.cpu_count()
    with concurrent.futures.ProcessPoolExecutor(num_children) as pool:
        futures = [pool.submit(forked_process, coro) for _ in range(num_children)]
        concurrent.futures.wait(futures)
