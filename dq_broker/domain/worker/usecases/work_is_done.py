import logging

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.domain.work.model import WorkEvent
from dq_broker.infrastructure.repositories.worker import WorkerRepository


log = logging.getLogger(__name__)


class WorkIsDoneDto:
    def __init__(self, worker_id, work_id, status, output=None):
        self.worker_id = worker_id
        self.work_id = work_id
        self.status = status
        self.output = output


class WorkIsDoneUsecase:
    def __init__(self, workers_repo: WorkerRepository, event_saver):
        self.workers_repo = workers_repo
        self.event_saver = event_saver

    async def perform(self, dto: WorkIsDoneDto):
        try:
            worker = self.workers_repo.get(dto.worker_id)
            worker.work_finished(dto.work_id)
            self.workers_repo.put(worker)
        except WorkerNotFound:
            log.warning(
                'Worker: %s not found in repository, '
                'but he finished work: %s with status: %s',
                dto.worker_id, dto.work_id, dto.status
            )
        finally:
            event = WorkEvent(
                work_id=dto.work_id,
                event_type='work_finished',
                work_status=dto.status,
                context={
                    'worker_id': dto.worker_id,
                    'output': dto.output,
                }
            )
            await self.event_saver.save_event(event)
