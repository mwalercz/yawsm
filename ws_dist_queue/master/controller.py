from collections import deque
from ws_dist_queue.message import WorkAcceptedMessage, WorkIsReadyMessage, WorkToBeDoneMessage, \
    WorkAcceptedNoWorkersMessage
from ws_dist_queue.model.work import Work


class MasterController:
    def __init__(self, message_sender, worker_picker):
        self.message_sender = message_sender
        self.picker = worker_picker
        self.workers = {}
        self.work_queue = deque()

    def worker_created(self, req):
        self.workers.update({
            req.sender.peer: Worker(req.sender, None)
        })

    def worker_down(self, req):
        if self.workers.get(req.sender.peer):
            dead_worker = self.workers[req.sender.peer]
            if dead_worker.current_work is not None:
                msg = 'worker: {} was dead while making job'.format(
                    req.sender.peer
                )
                print(msg)
                self.work_queue.appendleft(dead_worker.current_work)
                del self.workers[req.sender.peer]
                self.work(req)
            else:
                print('worker is dead')
                del self.workers[req.sender.peer]

    def work_is_done(self, req):
        self.workers[req.sender.peer].current_work = None

    def worker_requests_work(self, req):
        if len(self.work_queue) == 0:
            work = self.work_queue.pop()
            self.workers[req.sender.peer].current_work = work
            self.message_sender.send(req.sender, WorkToBeDoneMessage(work))

    def work(self, req):
        work = Work(
            command=req.message.command,
            cwd=req.message.cwd,
            username=req.session.username,
            password=req.session.password,
            work_id=1,
        )
        print(str(work))
        self.work_queue.appendleft(work)
        free_workers = self.picker.pick_best(
            [w for w in self.workers if w.current_job is None]
        )
        if free_workers:
            self.message_sender.send(
                req.sender,
                WorkAcceptedMessage(work.work_id)
            )
        else:
            self.message_sender.send(
                req.sender,
                WorkAcceptedNoWorkersMessage(work.work_id)
            )

        self._notify_workers(free_workers)

    def kill_work(self, req):
        work_found = filter(
            lambda work: work.work_id == req.message.work_id,
            self.work_queue
        )

    def list_work(self, req):
        work_found = filter(
            lambda work: work.work_id == req.message.work_id,
            self.work_queue
        )
        if work_found:
            return

    def _notify_workers(self, free_workers):
        if self.work_queue:
            for worker in free_workers:
                self.message_sender.send(worker.worker_ref, WorkIsReadyMessage())


class Worker:
    def __init__(self, worker_ref, current_work):
        self.worker_ref = worker_ref
        self.current_work = current_work


class WorkerPicker:
    def pick_best(self, workers):
        return workers
