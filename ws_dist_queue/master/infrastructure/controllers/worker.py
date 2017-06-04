import logging

from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import WorkIsDoneSchema

log = logging.getLogger(__name__)


class WorkerController:
    ROLE = 'worker'

    async def down(self, sender):
        peer = sender.peer
        dead_worker = self.workers.pop(peer, None)
        if not dead_worker:
            log.info('Worker: {peer} has died, but he wasnt registered'.format(peer=peer))
        dead_worker_work = dead_worker.current_work
        if not dead_worker_work:
            log.info('Worker: {peer} has died. He wasnt doing anything.'.format(peer=peer))
        log.info(
            'Worker: {peer} has died while working on: {work}'.format(
                peer=peer,
                work=dead_worker_work
            )
        )
        self.work_queue.push(dead_worker_work)
        await self._update_work_in_db(
            work_id=dead_worker_work['work_id'],
            status=WorkStatus.worker_failure.name,
        )

    def worker_created(self, req):
        self.workers.process_create_worker(
            req.sender.peer, Worker(req.sender, None)
        )
        self._notify_workers()

    @validate(schema=WorkIsDoneSchema)
    async def work_is_done(self, req):
        if not req.validated.status == WorkStatus.work_not_killed.name:
            self.workers[req.sender.peer].current_work = None

        await self._update_work_in_db(
            work_id=req.validated.work_id,
            status=req.validated.status,
            output=req.validated.output,
        )

    async def worker_requests_work(self, req):
        if len(self.work_queue) > 0:
            work = self.work_queue.pop()
            self.workers[req.sender.peer].current_work = work
            self.worker_client.send(
                recipient=req.sender,
                action_name='work_to_be_done',
                body=work,
            )
            await self._update_work_in_db(
                work_id=work['work_id'],
                status=WorkStatus.processing.name,
            )
