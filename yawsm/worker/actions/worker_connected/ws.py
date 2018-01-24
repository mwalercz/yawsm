from schematics import Model
from schematics.types import IntType, PolyModelType

from yawsm.infrastructure.websocket.request import validate
from yawsm.worker.model import SystemStat
from yawsm.worker.actions.worker_connected.usecase import NewWorkerDto


class NewWorkerSchema(Model):
    system_stat = PolyModelType(SystemStat, required=True)
    host_cpu_count = IntType(required=True)
    host_total_memory = IntType(required=True)


class WorkerConnectedController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=NewWorkerSchema)
    async def handle(self, request):
        validated = request.validated
        dto = NewWorkerDto(
            worker_socket=request.peer,
            worker_ref=request.sender,
            host_cpu_count=validated.host_cpu_count,
            host_total_memory=validated.host_total_memory,
            system_stat=validated.system_stat,
        )
        await self.usecase.perform(dto)
