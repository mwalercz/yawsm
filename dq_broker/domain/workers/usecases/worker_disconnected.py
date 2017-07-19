import logging

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.domain.work.model import WorkStatus, WorkEvent

log = logging.getLogger(__name__)


class WorkerDisconnectedUsecase:
    def __init__(
            self, workers_repo, work_queue, event_saver,
            workers_notifier
    ):
        self.workers_repo = workers_repo
        self.work_queue = work_queue
        self.event_saver = event_saver
        self.workers_notifier = workers_notifier

    async def perform(self, worker_id):
        try:
            worker = self.workers_repo.pop(worker_id)
        except WorkerNotFound as exc:
            log.exception(exc)
            return
        not_finished_work = worker.remove()
        if not_finished_work:
            self.work_queue.put(not_finished_work)
            self.workers_notifier.notify()
            event = WorkEvent(
                work_id=not_finished_work.work_id,
                event_type='worker_disconnected',
                work_status=WorkStatus.waiting_for_reschedule.name,
                context={'worker_id': worker_id}
            )
            await self.event_saver.save_event(
                event=event,
            )
