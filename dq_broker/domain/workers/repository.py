from typing import List

from copy import copy

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.domain.workers.model import Worker


class WorkersRepository:
    def __init__(self):
        self.workers = {}

    def put(self, worker):
        self.workers[worker.worker_id] = worker

    def remove(self, worker_id):
        del self.workers[worker_id]

    def get(self, worker_id) -> Worker:
        try:
            return copy(self.workers[worker_id])
        except KeyError:
            raise WorkerNotFound(worker_id)

    def pop(self, worker_id):
        try:
            return self.workers.pop(worker_id)
        except KeyError:
            raise WorkerNotFound(worker_id)

    def find_by_work_id(self, work_id):
        try:
            return [w for w in self.workers.values()
                    if w.current_work is not None and w.current_work.work_id == work_id][0]
        except IndexError:
            raise WorkerNotFound()

    def get_all_workers(self) -> List[Worker]:
        return [w for w in self.workers.values()]

    def get_free_workers(self):
        return [w for w in self.get_all_workers() if not w.has_work()]
