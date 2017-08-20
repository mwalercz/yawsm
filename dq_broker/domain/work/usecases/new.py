from dq_broker.domain.user.model import User
from dq_broker.domain.work.model import Work, Credentials
from dq_broker.domain.work.work_queue import WorkQueue
from dq_broker.domain.worker.notifier import WorkersNotifier
from dq_broker.infrastructure.http.controllers.schema import NewWorkDto
from dq_broker.infrastructure.repositories.work import WorkSaver


class NewWorkUsecase:
    def __init__(
            self,
            work_queue: WorkQueue,
            workers_notifier: WorkersNotifier,
            work_saver: WorkSaver
    ):
        self.work_queue = work_queue
        self.workers_notifier = workers_notifier
        self.work_saver = work_saver

    async def perform(self, new_work: NewWorkDto, user: User):
        db_work = await self.work_saver.save(new_work, user.user_id)
        work = Work(
            work_id=db_work.work_id,
            command=db_work.command,
            cwd=db_work.cwd,
            env=db_work.env,
            credentials=Credentials(
                username=user.username,
                password=user.password
            )
        )
        self.work_queue.put(work)
        await self.workers_notifier.notify()
        return work.work_id
