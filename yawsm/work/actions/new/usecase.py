import asyncio

from yawsm.infrastructure.repositories.work import WorkSaver
from yawsm.user.model import User
from yawsm.work.actions.dtos import NewWorkDto
from yawsm.work.model import Work, Credentials
from yawsm.work.work_queue import WorkQueue


class NewWorkUsecase:
    def __init__(
            self,
            work_queue: WorkQueue,
            task_queue: asyncio.Queue,
            work_saver: WorkSaver
    ):
        self.task_queue = task_queue
        self.work_queue = work_queue
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
        await self.task_queue.put(work)
        return work.work_id
