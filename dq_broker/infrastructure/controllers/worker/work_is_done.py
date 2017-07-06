from dq_broker.domain.workers.usecases.work_is_done import WorkIsDoneDto
from dq_broker.schema import WorkIsDoneSchema

from dq_broker.infrastructure.services.request import validate


class WorkIsDoneController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=WorkIsDoneSchema)
    async def handle(self, req):
        dto = WorkIsDoneDto(
            worker_id=req.peer,
            work_id=req.validated.work_id,
            status=req.validated.status,
            output=req.validated.output,
        )
        await self.usecase.perform(dto)
