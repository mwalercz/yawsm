from ws_dist_queue.master.domain.exceptions import WorkNotFound
from ws_dist_queue.master.domain.work.model import WorkStatus, FINAL_STATUSES, WorkEvent


class KillWorkUsecase:
    def __init__(
            self, work_queue, workers_repo,
            worker_client, work_finder, event_saver
    ):
        self.work_queue = work_queue
        self.workers_repo = workers_repo
        self.worker_client = worker_client
        self.event_saver = event_saver
        self.work_finder = work_finder

    async def perform(self, work_id, username):
        err = await self._validate(work_id, username)
        if err:
            return err

        try:
            self.work_queue.pop_by_id(work_id)
            event = WorkEvent(
                work_id=work_id,
                event_type='work_killed_in_queue',
                work_status=WorkStatus.killed.name,
            )
            self.event_saver.save_event(event)
            return {'status': 'work_killed_in_queue'}
        except WorkNotFound:
            worker = self.workers_repo.find_by_work_id(work_id)
            worker.remove_work()
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
            self.event_saver.save_event(event)
            return {
                'status': 'sig_kill_sent_to_worker',
                'worker_id': worker.worker_id,
            }

    async def _validate(self, work_id, username):
        work = await self.work_finder.find_by_work_id_and_username(work_id, username)
        if not work:
            return {
                'status': 'no_such_work_id_for_username'
            }
        if work.status in FINAL_STATUSES:
            return {
                'status': 'work_already_in_final_status',
                'work_status': work.status
            }
