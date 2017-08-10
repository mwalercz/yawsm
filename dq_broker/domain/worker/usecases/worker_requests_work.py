import logging

from dq_broker.domain.work.model import WorkEvent, WorkStatus


log = logging.getLogger(__name__)


class WorkerRequestsWorkUsecase:
    def __init__(self, work_queue, workers_repo, worker_client, event_saver):
        self.work_queue = work_queue
        self.workers_repo = workers_repo
        self.worker_client = worker_client
        self.event_saver = event_saver

    async def perform(self, worker_id):
        if self.work_queue.empty:
            log.info(
                'Worker: %s requested work, '
                'but work_queue is empty',
                worker_id
            )
            return
        work = self.work_queue.pop()
        worker = self.workers_repo.get(worker_id)
        worker.assign(work)
        self.workers_repo.put(worker)
        self.worker_client.send(
            recipient=worker.worker_ref,
            action_name='work_to_be_done',
            body=work.to_flat_dict(),
        )
        await self._update_work(work.work_id, worker_id)

    async def _update_work(self, work_id, worker_id):
        event = WorkEvent(
            work_id=work_id,
            event_type='work_assigned',
            work_status=WorkStatus.processing.name,
            context={'worker_id': worker_id}
        )
        await self.event_saver.save_event(
            work_event=event,
        )
