import logging

from ws_dist_queue.master.domain.exceptions import WorkerNotFound
from ws_dist_queue.master.domain.work.model import WorkEvent
from ws_dist_queue.master.domain.workers.repository import WorkersRepository


log = logging.getLogger(__name__)


class WorkIsDoneData:
    def __init__(self, worker_id, work_id, status, output=None):
        self.worker_id = worker_id
        self.work_id = work_id
        self.status = status
        self.output = output


class WorkIsDoneUsecase:
    def __init__(self, workers_repo: WorkersRepository, event_saver):
        self.workers_repo = workers_repo
        self.event_saver = event_saver

    async def perform(self, data: WorkIsDoneData):
        try:
            worker = self.workers_repo.get(data.worker_id)
            worker.work_finished(data.work_id)
        except WorkerNotFound:
            log.warning(
                'Worker: %s not found in repository, '
                'but he finished work: %s with status: %s',
                data.worker_id, data.work_id, data.status
            )
        finally:
            event = WorkEvent(
                work_id=data.work_id,
                event_type='work_finished',
                work_status=data.status,
                context={
                    'worker_id': data.worker_id,
                    'output': data.output,
                }
            )
            await self.event_saver.save_event(event)
