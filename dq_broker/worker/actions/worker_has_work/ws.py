from schematics import Model
from schematics.types import IntType, StringType, DictType

from dq_broker.infrastructure.websocket.request import validate
from dq_broker.work.model import Work, Credentials


class WorkerHasWorkSchema(Model):
    work_id = IntType(required=True)
    username = StringType(required=True)
    password = StringType(required=True)
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(field=StringType, required=True)


class WorkerHasWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=WorkerHasWorkSchema)
    async def handle(self, request):
        work = Work(
            work_id=request.validated.work_id,
            command=request.validated.command,
            env=request.validated.env,
            cwd=request.validated.cwd,
            credentials=Credentials(
                username=request.validated.username,
                password=request.validated.password,
            )
        )
        await self.usecase.perform(
            worker_socket=request.peer,
            work=work,
        )
