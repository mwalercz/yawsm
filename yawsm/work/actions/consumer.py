import asyncio
import logging

from yawsm.worker.notifier import WorkersNotifier

log = logging.getLogger(__name__)


class NewWorkConsumer:
    def __init__(
            self,
            workers_notifier: WorkersNotifier,
            queue: asyncio.Queue
    ):
        self.workers_notifier = workers_notifier
        self.queue = queue

    async def consume_all(self):
        while True:
            await self.consume_one()

    async def consume_one(self):
        await self.queue.get()
        try:
            await self.workers_notifier.notify()
        finally:
            self.queue.task_done()
