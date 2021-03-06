from schematics import Model
from schematics.types import IntType, StringType

from yawsm.infrastructure.websocket.request import validate
from yawsm.work.model import ALL_STATUSES
from yawsm.worker.actions.work_is_done.usecase import WorkIsDoneDto


class WorkIsDoneSchema(Model):
    work_id = IntType(required=True)
    status = StringType(
        required=True,
        choices=['KILLED', 'DONE']
    )
    output = StringType()
    exit_code = IntType()


class WorkIsDoneController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=WorkIsDoneSchema)
    async def handle(self, request):
        dto = WorkIsDoneDto(
            worker_socket=request.peer,
            work_id=request.validated.work_id,
            status=request.validated.status,
            output=request.validated.output,
            exit_code=request.validated.exit_code
        )
        await self.usecase.perform(dto)
