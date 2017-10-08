from dq_broker.infrastructure.repositories.worker import InMemoryWorkers
from dq_broker.worker.model import Worker, SystemStat


class WorkerDetailsUsecase:
    def __init__(self, workers: InMemoryWorkers):
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

    def _format_system_stat(self, system_stat: SystemStat):
        return system_stat.to_primitive()
