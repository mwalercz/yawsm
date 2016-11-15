import logging
import uuid

from collections import deque
from ws_dist_queue.message import WorkAcceptedMessage, WorkIsReadyMessage, WorkToBeDoneMessage, \
    WorkAcceptedNoWorkersMessage, KillWorkMessage, NoWorkWithGivenIdMessage, ListWorkResponseMessage
from ws_dist_queue.model.request import Request
from ws_dist_queue.model.work import Work


class MasterController:
    log = logging.getLogger(__name__)

    def __init__(self, message_sender, worker_picker):
        self.message_sender = message_sender
        self.picker = worker_picker
        self.workers = {}
        self.work_queue = deque()

    def worker_created(self, req):
        self.workers.update({
            req.sender.peer: Worker(req.sender, None)
        })
        self._notify_workers()

    def worker_down(self, req):
        if self.workers.get(req.sender.peer):
            dead_worker = self.workers[req.sender.peer]
            if dead_worker.current_work is not None:
                self.log.info(
                    'Worker: {peer} has died while working on: {work}'.format(
                        peer=req.sender.peer,
                        work=dead_worker.current_work
                    )
                )
                self.work_queue.appendleft(dead_worker.current_work)
            else:
                self.log.info(
                    'Worker: {peer} has died. He wasnt doing anything.'.format(
                        peer=req.sender.peer
                    )
                )
            del self.workers[req.sender.peer]

    def work_is_done(self, req):
        self.workers[req.sender.peer].current_work = None

    def worker_requests_work(self, req):
        if len(self.work_queue) > 0:
            work = self.work_queue.pop()
            self.workers[req.sender.peer].current_work = work
            self.message_sender.send(req.sender, WorkToBeDoneMessage(work))

    def work(self, req):
        work = WorkFactory.create(req)
        self.work_queue.appendleft(work)
        free_workers = self._get_free_workers()
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

        self._notify_workers()

    def kill_work(self, req):
        work_found = [w for w in self.workers.values()
                      if w.current_work is not None and
                      w.current_work.work_id == req.message.work_id]
        if work_found:
            self.message_sender.send(
                work_found[0].worker_ref,
                KillWorkMessage(req.message.work_id)
            )
        else:
            self.message_sender.send(
                req.sender,
                NoWorkWithGivenIdMessage(),
            )

    def work_was_killed(self, req):
        self.workers[req.sender.peer].current_work = None

    def list_work(self, req):
        found_in_workers = [w for w in self.workers.values()
                            if w.current_work is not None and
                            w.current_work.username == req.session.username]

        found_in_work_queue = [w for w in self.work_queue
                               if w.username == req.session.username]

        work_list = found_in_workers + found_in_work_queue
        self.message_sender.send(
            req.sender,
            ListWorkResponseMessage(work_list)
        )

    def _notify_workers(self):
        if self.work_queue:
            best_workers = self.picker.pick_best(self._get_free_workers())
            for worker in best_workers:
                self.message_sender.send(
                    worker.worker_ref, WorkIsReadyMessage())

    def _get_free_workers(self):
        return [w for w in self.workers.values() if w.current_work is None]


class Worker:
    def __init__(self, worker_ref, current_work):
        self.worker_ref = worker_ref
        self.current_work = current_work


class WorkerPicker:
    def pick_best(self, workers):
        return workers


class WorkFactory:
    @classmethod
    def create(cls, req):
        if isinstance(req, Request):
            work_id = uuid.uuid4()
            # WorkDB(
            #     command=req.message.command,
            #     cwd=req.message.cwd,
            #     username=req.session.username,
            #     password=req.session.password,
            #     work_id=work_id,
            # ).save()
            return Work(
                command=req.message.command,
                cwd=req.message.cwd,
                username=req.session.username,
                password=req.session.password,
                work_id=work_id,
            )
        elif isinstance(req, Work):
            return req
        else:
            raise RuntimeError()
