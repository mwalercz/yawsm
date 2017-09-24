from datetime import datetime

from dq_broker.domain.worker.model import SystemStat
from dq_broker.infrastructure.websocket.request import validate


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
