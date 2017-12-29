import logging

from dq_broker.exceptions import WorkNotFound, WorkerNotFound
from dq_broker.infrastructure.repositories.work import WorkFinder, WorkEventSaver
from dq_broker.infrastructure.repositories.worker import InMemoryWorkers
from dq_broker.infrastructure.websocket.clients import WorkerClient
from dq_broker.work.model import (
    WorkStatus,
    WorkEvent,
    KillWork,
    FINAL_STATUSES,
    WORK_IN_WORK_QUEUE_STATUSES,
    WORK_PROCESSED_BY_WORKER_STATUSES,
)
from dq_broker.work.work_queue import WorkQueue

log = logging.getLogger(__name__)


class KillWorkUsecase:
    def __init__(
            self,
            work_queue: WorkQueue,
            workers: InMemoryWorkers,
            worker_client: WorkerClient,
            work_finder: WorkFinder,
            event_saver: WorkEventSaver,
    ):
        self.work_queue = work_queue
        self.workers = workers
        self.worker_client = worker_client
        self.event_saver = event_saver
        self.work_finder = work_finder

    async def perform(self, dto: KillWork):
        try:
            work = await self.work_finder.find_by_work_id_and_user_id(
                dto.work_id, dto.user_id
            )
        except WorkNotFound:
            return self._error('work_not_found_in_db')

        if work.status == WorkStatus.unknown.name:
            return self._error(
                'work_in_unknown_status',
                detailed_reson=(
                    'Broker was restarted and all unfinished works '
                    'went to "unknown" status. '
                    'If there was a worker which was working on this '
                    'work, and he didn\'t die during broker unavailability '
                    'then work should be moved to "processing" status '
                    'after this concrete worker reconnects.'
                    'Otherwise, this work will be stuck in "unknown" status.'
                )
            )
        if work.status in FINAL_STATUSES:
            return self._error(
                'work_already_in_final_status',
                work_status=work.status,
            )

        if work.status in WORK_IN_WORK_QUEUE_STATUSES:
            try:
                self.work_queue.pop_by_id(dto.work_id)
            except WorkNotFound:
                detailed_reason = (
                    'Work id: {} is in {} status, which means. '
                    'that it should be in in-memory work queue.'
                    'But it was not found there.'.format(
                        work.work_id,
                        work.status,
                    )
                )
                log.error(detailed_reason)
                return self._unexpected_error(
                    'work_not_found_in_work_queue',
                    detailed_reason=detailed_reason
                )
            else:
                info = 'work_cancelled_in_queue'
                event = WorkEvent(
                    work_id=dto.work_id,
                    reason=info,
                    work_status=WorkStatus.cancelled.name,
                )
                await self.event_saver.save_event(event)
                return self._ok(info)

        if work.status in WORK_PROCESSED_BY_WORKER_STATUSES:
            try:
                worker = self.workers.find_by_work_id(dto.work_id)
            except WorkerNotFound:
                detailed_reason = (
                    'Work id: {} is in {} status, which means '
                    'that one in-memory worker should be assigned to it. '
                    'No such worker was found.'.format(
                        work.work_id,
                        work.status
                    )
                )
                log.error(detailed_reason)
                return self._unexpected_error(
                    'no_worker_assigned_to_work',
                    detailed_reason=detailed_reason
                )
            else:
                self.worker_client.send(
                    recipient=worker.worker_ref,
                    action_name='cancel_work',
                )
                info = 'cancel_work_sent_to_worker'
                context = {'worker_socket': worker.worker_socket}
                event = WorkEvent(
                    work_id=dto.work_id,
                    reason=info,
                    work_status=WorkStatus.to_be_cancelled.name,
                    context=context
                )
                await self.event_saver.save_event(event)
                return self._ok(info, **context)

    def _ok(self, info, **context):
        return {
            'status': 'ok',
            'info': info,
            **context
        }

    def _error(self, reason, **context):
        return {
            'status': 'error',
            'reason': reason,
            **context
        }

    def _unexpected_error(self, *args, **kwargs):
        return self._error(*args, **kwargs)
