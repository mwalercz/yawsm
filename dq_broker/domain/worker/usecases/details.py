from dq_broker.domain.worker.model import Worker
from dq_broker.infrastructure.repositories.worker import WorkerRepository
from dq_broker.infrastructure.websocket.controllers.worker.worker_system_stat import WorkerSystemStat


class WorkerDetailsUsecase:
    def __init__(self, workers: WorkerRepository):
        self.workers = workers

    async def perform(self, worker_socket):
        worker = self.workers.get(worker_socket)
        return self._format_worker(worker)

    def _format_worker(self, worker: Worker):
        return {
            'worker_socket': worker.worker_socket,
            'current_work': worker.current_work,
            'system_stats': [
                self._format_system_stat(system_stat)
                for system_stat in worker.system_stats
            ]
        }

    def _format_system_stat(self, system_stat: WorkerSystemStat):
        return system_stat.to_primitive()
