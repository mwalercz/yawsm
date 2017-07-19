from dq_broker.domain.work.model import Work, CommandData
from dq_broker.infrastructure.auth.user import Credentials
from dq_broker.infrastructure.websocket.controllers.schema import WorkerHasWorkSchema
from dq_broker.infrastructure.websocket.request import validate


class WorkerHasWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=WorkerHasWorkSchema)
    async def handle(self, request):
        work = Work(
            work_id=request.validated.work_id,
            command_data=CommandData(
                command=request.validated.command,
                env=request.validated.env,
                cwd=request.validated.cwd,
            ),
            credentials=Credentials(
                username=request.validated.username,
                password=request.validated.password,
            )
        )
        await self.usecase.perform(
            worker_id=request.peer,
            work=work,
        )
