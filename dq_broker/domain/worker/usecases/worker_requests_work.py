import logging

from dq_broker.domain.exceptions import InvalidStateException
from dq_broker.domain.work.model import WorkEvent, WorkStatus


log = logging.getLogger(__name__)


class WorkerRequestsWorkUsecase:
    def __init__(self, work_queue, workers, worker_client, event_saver, notifier):
        self.work_queue = work_queue
        self.workers = workers
        self.worker_client = worker_client
        self.event_saver = event_saver
        self.notifier = notifier

    async def perform(self, worker_socket):
        if self.work_queue.empty:
            log.info(
                'Worker: %s requested work, '
                'but work_queue is empty',
                worker_socket
            )
            return
        work = self.work_queue.pop()
        worker = self.workers.get(worker_socket)
        try:
            worker.assign(work)
        except InvalidStateException as exc:
            log.exception('Putting work back to queue', exc_info=1)
            self.work_queue.put(work)
            await self.notifier.notify()
            return
        self.workers.put(worker)
        self.worker_client.send(
            recipient=worker.worker_ref,
            action_name='work_to_be_done',
            body={
                'work_id': work.work_id,
                'cwd': work.cwd,
                'command': work.command,
                'env': work.env,
                'username': work.credentials.username,
                'password': work.credentials.password,
            },
        )
        await self._update_work(work.work_id, worker_socket)

    async def _update_work(self, work_id, worker_socket):
        event = WorkEvent(
            work_id=work_id,
            event_type='work_assigned',
            work_status=WorkStatus.processing.name,
            context={'worker_socket': worker_socket}
        )
        await self.event_saver.save_event(
            work_event=event,
        )
