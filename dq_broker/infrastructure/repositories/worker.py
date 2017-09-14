from typing import List

from copy import copy

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.domain.worker.model import Worker


class InMemoryWorkers:
    def __init__(self):
        self.workers = {}

    def put(self, worker):
        self.workers[worker.worker_socket] = worker

    def remove(self, worker_socket):
        del self.workers[worker_socket]

    def get(self, worker_socket) -> Worker:
        try:
            return copy(self.workers[worker_socket])
        except KeyError:
            raise WorkerNotFound(worker_socket)

    def pop(self, worker_socket):
        try:
            return self.workers.pop(worker_socket)
        except KeyError:
            raise WorkerNotFound(worker_socket)

    def find_by_work_id(self, work_id):
        try:
            return [w for w in self.workers.values()
                    if w.current_work is not None and w.current_work.work_id == work_id][0]
        except IndexError:
            raise WorkerNotFound()

    def get_all_workers(self) -> List[Worker]:
        return [w for w in self.workers.values()]

    def get_free_workers(self):
        return {
            socket: worker for socket, worker
            in self.workers.items()
            if not worker.has_work()
        }
