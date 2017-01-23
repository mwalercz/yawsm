import logging
from collections import deque

from playhouse.shortcuts import model_to_dict

from ws_dist_queue.master.components.authorization import UserAuthorization
from ws_dist_queue.master.components.clients import UserClient, WorkerClient
from ws_dist_queue.master.components.validator import validate
from ws_dist_queue.master.controllers.base import BaseController

from ws_dist_queue.master.models.work import Work, WorkStatus
from ws_dist_queue.master.schema import WorkIdSchema, NewWorkSchema

log = logging.getLogger(__name__)


class UserController(BaseController):
    ROLE = 'user'

    def __init__(
            self, work_queue: deque, workers: dict,
            objects, picker, worker_client: WorkerClient,
            user_client: UserClient, user_auth: UserAuthorization
    ):
        super().__init__(
            work_queue, workers, objects, picker, worker_client, user_client
        )
        self.user_auth = user_auth

    @validate(schema=NewWorkSchema)
    async def new_work(self, req):
        session = self.user_auth.get_session(req.sender.peer)
        work_db = await self.objects.create(
            Work,
            command=req.validated.command,
            cwd=req.validated.cwd,
            env=req.validated.env,
            username=session.username,
            status=WorkStatus.received.name,
        )
        work = {
            'work_id': work_db.work_id,
            'command': work_db.command,
            'cwd': work_db.cwd,
            'env': work_db.env,
            'username': session.username,
            'password': session.password,
        }

        self.work_queue.appendleft(work)
        free_workers = self._get_free_workers()
        if free_workers:
            self.user_client.send(
                recipient=req.sender,
                info='Work accepted',
                body=model_to_dict(work_db),
            )
        else:
            self.user_client.send(
                recipient=req.sender,
                info='Work accepted, no workers',
                body=model_to_dict(work_db),
            )

        self._notify_workers()

    @validate(schema=WorkIdSchema)
    async def kill_work(self, req):
        work_id = req.validated.work_id
        worker_found = self._get_worker_with_work(work_id)
        if worker_found:
            self.worker_client.send(
                recipient=worker_found.worker_ref,
                action_name='kill_work',
                body={
                    'work_id': work_id,
                }
            )
            self.user_client.send(
                recipient=req.sender,
                info='SIG kill was send to worker. Check later',
            )
        else:
            work = self._pop_work_from_queue(work_id)
            if work:
                work_db = await self._update_status_in_db(
                    work_id=work_id,
                    status=WorkStatus.work_killed.name
                )
                self.user_client.send(
                    recipient=req.sender,
                    info='Work with (id: {0}) was killed'.format(work_id),
                    body=model_to_dict(work_db),
                )
            else:
                self.user_client.send(
                    recipient=req.sender,
                    info='No work with (id: {0}) in progress'.format(work_id)
                )

    async def list_work(self, req):
        session = self.user_auth.get_session(req.sender.peer)
        work_cursor = await self.objects.execute(
            Work.select()
                .where(Work.username == session.username)
                .order_by(Work.work_id)
        )
        work_list = [model_to_dict(w) for w in work_cursor]
        self.user_client.send(
            recipient=req.sender,
            info='User work list',
            body=work_list
        )

    def _get_worker_with_work(self, work_id):
        for w in self.workers.values():
            if w.current_work is not None and w.current_work.work_id == work_id:
                return w
        return None

    def _pop_work_from_queue(self, work_id):
        work_found = None
        for work in self.work_queue:
            if work.work_id == work_id:
                work_found = work
                break

        if work_found:
            self.work_queue.remove(work_found)
            return work_found
        else:
            return None

