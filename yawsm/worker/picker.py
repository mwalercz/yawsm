import asyncio
from typing import List

from yawsm.worker.model import Worker


class FreeWorkersPicker:
    async def pick_best(self, workers: List[Worker]):
        for w in workers:
            yield w


class SystemInfoBasedPicker:
    def __init__(self, delay):
        self.delay = delay

    async def pick_best(self, workers: List[Worker]):
        sorted_by_avg_load = sorted(
            workers,
            key=lambda w: w.host.avg_available_load,
            reverse=True,
        )
        for worker in sorted_by_avg_load:
            yield worker
            asyncio.sleep(self.delay)
