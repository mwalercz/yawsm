from dq_broker.infrastructure.repositories.worker import InMemoryWorkers
from dq_broker.worker.model import Worker


class WorkerListUsecase:
    def __init__(self, workers: InMemoryWorkers):
        self.workers = workers

    async def perform(self):
        workers = self.workers.get_all_workers()
        formatted_workers = [
            self._format_worker(worker)
            for worker in workers
            ]
        return formatted_workers

    def _format_worker(self, worker: Worker):
        return {
            'worker_socket': worker.worker_socket,
            'current_work': worker.current_work,
            **self._format_avg_stats(worker)
        }

    def _format_avg_stats(self, worker):
        return {
            'avg_available_load': worker.host.avg_available_load,
            'avg_available_memory': worker.host.avg_available_memory
        }
