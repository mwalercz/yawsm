import logging
from typing import NamedTuple, Any

from dq_broker.domain.worker.model import Worker, SystemStat, Host

log = logging.getLogger(__name__)


class NewWorkerDto(NamedTuple):
    worker_socket: str
    worker_ref: Any
    host_cpu_count: int
    host_total_memory: int
    system_stat: SystemStat


class WorkerConnectedUsecase:
    def __init__(
            self,
            workers,
            hosts,
            workers_notifier,
    ):
        self.hosts = hosts
        self.workers = workers
        self.workers_notifier = workers_notifier

    async def perform(self, dto: NewWorkerDto):
        host_address = self._extract_host_address(dto.worker_socket)
        host, created = self.hosts.get_or_create(
            Host(
                host_address=host_address,
                cpu_count=dto.host_cpu_count,
                total_memory=dto.host_total_memory,
            )
        )
        worker = Worker(
            worker_socket=dto.worker_socket,
            worker_ref=dto.worker_ref,
            host=host,
        )
        worker.add_system_stat(dto.system_stat)
        self.workers.put(worker)
        await self.workers_notifier.notify()
        log.info('New worker: %s connected', worker.worker_socket)

    def _extract_host_address(self, socket):
        return socket
