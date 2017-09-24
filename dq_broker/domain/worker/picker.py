from typing import List, Dict

import asyncio
import functools

from dq_broker.domain.worker.model import Worker


class FreeWorkersPicker:
    async def pick_best(self, workers: Dict[str, Worker]):
        for w in workers.values():
            yield w
            await asyncio.sleep(0.5)


class SystemInfoBasedPicker:
    def __init__(self, delay, workers_repo):
        self.delay = delay
        self.workers_repo = workers_repo

    async def pick_best(self, workers: Dict[str, Worker]):
        worker_ids = []
        workers_system_stats = self.workers_repo.system_stats(
            start='lala', worker_ids=worker_ids
        )
        sorted_workers = sorted(
            workers,
            key=functools.cmp_to_key(self.cmp),
        )
        for worker in sorted_workers:
            yield worker
            asyncio.sleep(self.delay)

    def cmp(self, one, other):
        if self.compute_usage(one) > self.compute_usage(other):
            return 1
        else:
            return -1

    def compute_usage(self, worker: Worker):
        sum = 0
        number_of_elements = 0
        for system_info in worker.system_stats[-100:]:
            sum += system_info.cpu.percent * system_info.cpu.count
            number_of_elements += 1

        average_usage = float(sum) / float(number_of_elements)
        return average_usage
