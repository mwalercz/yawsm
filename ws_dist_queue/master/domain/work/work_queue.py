import collections

from ws_dist_queue.master.domain.exceptions import WorkNotFound


class WorkQueue:
    def __init__(self, work_queue: collections.OrderedDict):
        self.queue = work_queue

    def put(self, work):
        self.queue[work.work_id] = work

    def pop(self):
        k, v = self.queue.popitem(last=False)
        return v

    def pop_by_id(self, work_id):
        try:
            return self.queue.pop(work_id)
        except KeyError:
            raise WorkNotFound(work_id)

    @property
    def empty(self):
        return not self.queue
