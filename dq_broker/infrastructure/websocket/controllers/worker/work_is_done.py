from schematics import Model
from schematics.types import IntType, StringType

from dq_broker.domain.work.model import ALL_WORK_STATUSES
from dq_broker.domain.workers.usecases.work_is_done import WorkIsDoneDto

from dq_broker.infrastructure.websocket.request import validate


class WorkIsDoneSchema(Model):
    work_id = IntType(required=True)
    status = StringType(
        required=True,
        choices=ALL_WORK_STATUSES
    )
    output = StringType()


class WorkIsDoneController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=WorkIsDoneSchema)
    async def handle(self, request):
        dto = WorkIsDoneDto(
            worker_id=request.peer,
            work_id=request.validated.work_id,
            status=request.validated.status,
            output=request.validated.output,
        )
        await self.usecase.perform(dto)
