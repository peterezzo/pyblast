#!/usr/bin/env python3
"""
Test harness for lib split
"""
import asyncio
import collections
import os
from pyblast import task_runner, work_queue, result_queue


async def async_task(id):
    pid = os.getpid()
    print(f'start async_task for {id} in {pid}')
    await asyncio.sleep(5)
    print(f'end async_task for {id} in {pid}')
    result_queue.put((id, pid))


def main(args):
    print(f'main process is {os.getpid()}')

    task_args = range(1000)
    [work_queue.put(a) for a in task_args]
    task_runner(async_task)

    counts = collections.Counter()
    for _ in range(len(task_args)):
        result, pid = result_queue.get()
        counts[pid] += 1
    print(counts)

    print('main process end')


def parse_args():
    pass


if __name__ == '__main__':
    args = parse_args()
    main(args)
