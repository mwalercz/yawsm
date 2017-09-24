import logging
from typing import NamedTuple, Any

from dq_broker.domain.worker.model import Worker
from dq_broker.domain.worker.models.host import Host
from dq_broker.domain.worker.repository import WorkersRepository

log = logging.getLogger(__name__)


class NewWorkerDto(NamedTuple):
    worker_socket: str
    worker_ref: Any
    host_cpu_count: int
    host_total_memory: int
    host_total_memory: int


class WorkerConnectedUsecase:
    def __init__(
            self,
            workers,
            hosts,
            workers_notifier,
            workers_repo: WorkersRepository
    ):
        self.hosts = hosts
        self.workers_repo = workers_repo
        self.workers = workers
        self.workers_notifier = workers_notifier

    async def perform(self, dto: NewWorkerDto):
        host_address = self._extract_host_address(dto.worker_socket)
        host = await self.hosts.get_or_create(
            Host(
                host_address=host_address
            )
        )
        worker = Worker(
            worker_socket=dto.worker_socket,
            worker_ref=dto.worker_ref,
            host=host,
        )
        self.workers.put(worker)
        await self.workers_notifier.notify()
        log.info('New worker: %s connected', worker.worker_socket)

    def _extract_host_address(self, socket):
        return socket
