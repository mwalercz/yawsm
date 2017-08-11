from dq_broker.domain.user.model import User
from dq_broker.domain.work.model import Work, CommandData
from dq_broker.domain.work.work_queue import WorkQueue
from dq_broker.domain.worker.notifier import WorkersNotifier
from dq_broker.infrastructure.auth.user import Credentials
from dq_broker.infrastructure.http.controllers.schema import NewWorkSchema
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

    async def perform(self, new_work: NewWorkSchema, user: User):
        work = Work.new(
            command_data=CommandData(
                command=new_work.command,
                env=new_work.env,
                cwd=new_work.cwd,
            ),
            credentials=Credentials(
                username=user.username,
                password=user.password,
            )
        )
        work_id = await self.work_saver.save(work, user.user_id)
        work.set_id(work_id)
        self.work_queue.put(work)
        await self.workers_notifier.notify()
        return work_id
