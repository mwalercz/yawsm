from collections import deque

from ws_dist_queue.master.components.clients import WorkerClient, UserClient
from ws_dist_queue.master.models.work import Work


class BaseController:
    def __init__(
            self, work_queue: deque, workers: dict, objects,
            picker, worker_client: WorkerClient, user_client: UserClient,

    ):
        self.work_queue = work_queue
        self.workers = workers
        self.picker = picker
        self.worker_client = worker_client
        self.user_client = user_client
        self.objects = objects

    def down(self, sender):
        pass

    def _notify_workers(self):
        if self.work_queue:
            best_workers = self.picker.pick_best(self._get_free_workers())
            for worker in best_workers:
                self.worker_client.send(
                    recipient=worker.worker_ref,
                    action_name='work_is_ready'
                )

    def _get_free_workers(self):
        return [w for w in self.workers.values() if w.current_work is None]

    async def _update_work_in_db(self, work_id, **fields):
        work_db = await self.objects.get(Work, work_id=work_id)
        for field, value in fields.items():
            setattr(work_db, field, value)
        await self.objects.update(work_db)
        return work_db


class Worker:
    def __init__(self, worker_ref, current_work):
        self.worker_ref = worker_ref
        self.current_work = current_work


class WorkerPicker:
    def pick_best(self, workers):
        return workers
