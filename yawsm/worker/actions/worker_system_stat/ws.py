from yawsm.infrastructure.websocket.request import validate
from yawsm.worker.model import SystemStat


class WorkerSystemStatController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=SystemStat)
    async def handle(self, request):
        system_stat = request.validated
        await self.usecase.perform(
            worker_socket=request.peer,
            system_stat=system_stat,
        )
