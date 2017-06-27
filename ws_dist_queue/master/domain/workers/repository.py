from ws_dist_queue.master.domain.exceptions import WorkerNotFound


class WorkersRepository:
    def __init__(self):
        self.workers = {}

    def put(self, worker):
        self.workers[worker.worker_id] = worker

    def remove(self, worker_id):
        del self.workers[worker_id]

    def get(self, worker_id):
        try:
            return self.workers[worker_id]
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

    def all(self):
        return [w for w in self.workers.values()]
