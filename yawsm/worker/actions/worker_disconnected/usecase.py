import logging

from yawsm.exceptions import WorkerNotFound
from yawsm.work.model import WorkStatus, WorkEvent

log = logging.getLogger(__name__)


class WorkerDisconnectedUsecase:
    def __init__(
            self, workers, work_queue, event_saver,
            workers_notifier
    ):
        self.workers = workers
        self.work_queue = work_queue
        self.event_saver = event_saver
        self.workers_notifier = workers_notifier

    async def perform(self, worker_socket):
        try:
            worker = self.workers.pop(worker_socket)
        except WorkerNotFound as exc:
            log.exception(exc)
            return
        not_finished_work = worker.remove()
        if not_finished_work:
            self.work_queue.put(not_finished_work)
            await self.workers_notifier.notify()
            event = WorkEvent(
                work_id=not_finished_work.work_id,
                reason='worker_disconnected',
                work_status=WorkStatus.READY.name,
                context={'worker_socket': worker_socket}
            )
            await self.event_saver.save_event(
                event=event,
            )
