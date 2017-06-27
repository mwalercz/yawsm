from ws_dist_queue.master.domain.workers.usecases.work_is_done import WorkIsDoneDto
from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import WorkIsDoneSchema


class WorkIsDoneController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=WorkIsDoneSchema)
    async def handle(self, req):
        data = WorkIsDoneDto(
            worker_id=req.sender.peer,
            work_id=req.validated.work_id,
            status=req.validated.status,
            output=req.validated.output,
        )
        await self.usecase.perform(data)
