import logging
from typing import NamedTuple, Any

from dq_broker.domain.worker.model import Worker
from dq_broker.domain.worker.repository import WorkersRepository

log = logging.getLogger(__name__)


class NewWorkerDto(NamedTuple):
    worker_socket: str
    worker_ref: Any


class WorkerConnectedUsecase:
    def __init__(
            self,
            workers,
            workers_notifier,
            workers_repo: WorkersRepository
    ):
        self.workers_repo = workers_repo
        self.workers = workers
        self.workers_notifier = workers_notifier

    async def perform(self, dto: NewWorkerDto):
        host_address = self._extract_host_address(dto.worker_socket)
        host = await self.workers_repo.get_or_create_host(host_address)
        worker_id = await self.workers_repo.create_worker(
            worker_socket=dto.worker_socket,
            host=host,
        )
        worker = Worker(
            worker_id=worker_id,
            worker_socket=dto.worker_socket,
            worker_ref=dto.worker_ref,
            host_id=host.host_id,
        )
        self.workers.put(worker)
        await self.workers_notifier.notify()
        log.info('New worker: %s connected', worker.worker_socket)

    def _extract_host_address(self, socket):
        return socket
