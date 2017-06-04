import logging

log = logging.getLogger(__name__)


class WorkerConnectedUsecase:
    def __init__(self, workers_repo, workers_notifier):
        self.workers_repo = workers_repo
        self.workers_notifier = workers_notifier

    def perform(self, worker):
        self.workers_repo.put(worker)
        self.workers_notifier.notify()
        log.info('New worker: %s connected', worker.worker_id)
