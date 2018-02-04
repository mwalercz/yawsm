import logging

from yawsm.exceptions import WorkerNotFound
from yawsm.infrastructure.repositories.worker import InMemoryWorkers
from yawsm.work.model import WorkEvent, WorkStatus

log = logging.getLogger(__name__)


class WorkIsDoneDto:
    def __init__(self, worker_socket, work_id, status, exit_code=None, output=None):
        self.worker_socket = worker_socket
        self.work_id = work_id
        self.status = status
        self.output = output
        self.exit_code = exit_code


class WorkIsDoneUsecase:
    def __init__(self, worker_client, workers: InMemoryWorkers, event_saver):
        self.worker_client = worker_client
        self.workers = workers
        self.event_saver = event_saver

    async def perform(self, dto: WorkIsDoneDto):
        try:
            worker = self.workers.get(dto.worker_socket)
            worker.work_finished(dto.work_id)
            self.workers.put(worker)
        except WorkerNotFound:
            log.exception(
                'Worker: %s not found in repository, '
                'but he FINISHED work: %s with status: %s',
                dto.worker_socket, dto.work_id, dto.status
            )
        else:
            self.worker_client.send(
                recipient=worker.worker_ref,
                action_name='work_is_done_ack',
            )
        finally:
            work_status, reason = self._resolve_work_status(dto)
            event = WorkEvent(
                work_id=dto.work_id,
                reason=reason,
                work_status=work_status,
                context={
                    'worker_socket': dto.worker_socket,
                }
            )
            await self.event_saver.save_event(
                event,
                output=dto.output,
                exit_code=dto.exit_code,
            )

    def _resolve_work_status(self, dto):
        if dto.status == 'DONE':
            if dto.exit_code == 0:
                return WorkStatus.FINISHED.name, 'work_finished_with_success'
            else:
                return WorkStatus.ERROR.name, 'work_finished_with_error'
        elif dto.status == 'KILLED':
            return WorkStatus.CANCELLED.name, 'work_cancelled'
        else:
            raise Exception(
                'Wrong status, work_id: %s, status: %',
                dto.work_id, dto.status
            )
