from dq_broker.domain.exceptions import WorkNotFound

from dq_broker.domain.work.model import WorkStatus, FINAL_STATUSES, WorkEvent
from dq_broker.domain.work.work_queue import WorkQueue
from dq_broker.infrastructure.repositories.work import WorkFinder, WorkEventSaver
from dq_broker.infrastructure.repositories.worker import WorkerRepository
from dq_broker.infrastructure.websocket.clients import WorkerClient


class KillWorkUsecase:
    def __init__(
            self,
            work_queue: WorkQueue,
            worker_repo: WorkerRepository,
            worker_client: WorkerClient,
            work_finder: WorkFinder,
            event_saver: WorkEventSaver,
    ):
        self.work_queue = work_queue
        self.workers_repo = worker_repo
        self.worker_client = worker_client
        self.event_saver = event_saver
        self.work_finder = work_finder

    async def perform(self, work_id, user_id):
        err = await self._validate(work_id, user_id)
        if err:
            return err

        try:
            self.work_queue.pop_by_id(work_id)
            event = WorkEvent(
                work_id=work_id,
                event_type='work_killed_in_queue',
                work_status=WorkStatus.killed.name,
            )
            await self.event_saver.save_event(event)
            return {'status': 'work_killed_in_queue'}
        except WorkNotFound:
            worker = self.workers_repo.find_by_work_id(work_id)
            self.worker_client.send(
                recipient=worker.worker_ref,
                action_name='kill_work',
            )
            event = WorkEvent(
                work_id=work_id,
                event_type='sig_kill_sent_to_worker',
                work_status=WorkStatus.to_be_killed.name,
                context={'worker_id': worker.worker_id}
            )
            await self.event_saver.save_event(event)
            return {
                'status': 'sig_kill_sent_to_worker',
                'worker_id': worker.worker_id,
            }

    async def _validate(self, work_id, user_id):
        try:
            work = await self.work_finder.find_by_work_id_and_user_id(
                work_id, user_id
            )
        except WorkNotFound:
            return {
                'status': 'work_does_not_exist'
            }
        if work.status in FINAL_STATUSES:
            return {
                'status': 'work_already_in_final_status',
                'work_status': work.status
            }



