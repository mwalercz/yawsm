from dq_broker.domain.worker.model import Worker
from dq_broker.infrastructure.repositories.worker import InMemoryWorkers
from dq_broker.infrastructure.websocket.controllers.worker.worker_system_stat import WorkerSystemStat


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
            'last_system_stat': self._format_system_stat(
                worker.get_last_system_stat()
            )
        }

    def _format_system_stat(self, system_stat: WorkerSystemStat):
        if system_stat:
            return system_stat.to_primitive()
        else:
            return None