import logging

from collections import deque
from playhouse.shortcuts import model_to_dict
from ws_dist_queue.domain.work import Work
from ws_dist_queue.messages import Message
from ws_dist_queue.model.work import WorkStatus


class MasterController:
    log = logging.getLogger(__name__)

    def __init__(self, message_sender, worker_picker, objects):
        self.message_sender = message_sender
        self.picker = worker_picker
        self.objects = objects
        self.workers = {}
        self.work_queue = deque()

    def worker_created(self, req):
        self.workers.update({
            req.sender.peer: Worker(req.sender, None)
        })
        self._notify_workers()

    async def worker_down(self, req):
        if self.workers.get(req.sender.peer):
            dead_worker = self.workers[req.sender.peer]
            worker_work = dead_worker.current_work
            if worker_work is not None:
                self.log.info(
                    'Worker: {peer} has died while working on: {work}'.format(
                        peer=req.sender.peer,
                        work=worker_work
                    )
                )
                worker_work.status = WorkStatus.worker_failure
                await self.objects.update(worker_work)
                self.work_queue.appendleft(dead_worker.current_work)
            else:
                self.log.info(
                    'Worker: {peer} has died. He wasnt doing anything.'.format(
                        peer=req.sender.peer
                    )
                )
            del self.workers[req.sender.peer]

    async def work_is_done(self, req):
        finished_work = self.workers[req.sender.peer].current_work
        finished_work.status = req.message.status
        await self.objects.update(finished_work)

        self.workers[req.sender.peer].current_work = None

    async def worker_requests_work(self, req):
        if len(self.work_queue) > 0:
            work = self.work_queue.pop()
            self.workers[req.sender.peer].current_work = work
            self.message_sender.send(req.sender, Message.work_to_be_done, model_to_dict(work))
            work.status = WorkStatus.processing
            await self.objects.update(work)

    async def new_work(self, req):
        self.log.info(req)
        work = await self.objects.create(
            Work,
            command=req.message.command,
            cwd=req.message.cwd,
            env=req.message.env,
            status=WorkStatus.received.name,
            username=req.session.username,
            password=req.session.password
        )
        self.work_queue.appendleft(work)
        free_workers = self._get_free_workers()
        if free_workers:
            self.message_sender.send(
                req.sender,
                Message.work_accepted,
                model_to_dict(work, exclude=['username', 'password'])
            )
        else:
            self.message_sender.send(
                req.sender,
                Message.work_accepted_no_worker,
                model_to_dict(work, exclude=['username', 'password'])
            )

        self._notify_workers()

    def kill_work(self, req):
        work_found = [w for w in self.workers.values()
                      if w.current_work is not None and
                      w.current_work.work_id == req.message.work_id]
        if work_found:
            self.message_sender.send(
                work_found[0].worker_ref,
                Message.kill_work,
                {'work_id': req.message.work_id}
            )
        else:
            self.message_sender.send(
                req.sender,
                Message.no_work_with_given_id,
            )

    def work_was_killed(self, req):
        self.workers[req.sender.peer].current_work = None

    async def list_work(self, req):
        # found_in_workers = [w for w in self.workers.values()
        #                     if w.current_work is not None and
        #                     w.current_work.username == req.session.username]
        #
        # found_in_work_queue = [w for w in self.work_queue
        #                        if w.username == req.session.username]
        work_list = self.objects.get(Work, username=req.session.username)
        self.message_sender.send(
            req.sender,
            Message.list_work_response,
            work_list
        )

    def _notify_workers(self):
        if self.work_queue:
            best_workers = self.picker.pick_best(self._get_free_workers())
            for worker in best_workers:
                self.message_sender.send(
                    worker.worker_ref, Message.work_is_ready)

    def _get_free_workers(self):
        return [w for w in self.workers.values() if w.current_work is None]


class Worker:
    def __init__(self, worker_ref, current_work):
        self.worker_ref = worker_ref
        self.current_work = current_work


class WorkerPicker:
    def pick_best(self, workers):
        return workers

