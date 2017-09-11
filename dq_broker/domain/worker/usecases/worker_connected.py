import logging

log = logging.getLogger(__name__)


class WorkerConnectedUsecase:
    def __init__(self, workers, workers_notifier):
        self.workers = workers
        self.workers_notifier = workers_notifier

    async def perform(self, worker):
        self.workers.put(worker)
        await self.workers_notifier.notify()
        log.info('New worker: %s connected', worker.worker_id)
