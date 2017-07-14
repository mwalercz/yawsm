from dq_broker.domain.workers.usecases.work_is_done import WorkIsDoneDto
from infrastructure.websocket.controllers.schema import WorkIsDoneSchema

from infrastructure.websocket.request import validate


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
