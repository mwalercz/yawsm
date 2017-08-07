from schematics import Model
from schematics.types import IntType, FloatType, PolyModelType, DateTimeType

from dq_broker.infrastructure.websocket.request import validate


class Cpu(Model):
    count = IntType(required=True)
    percent = FloatType(required=True)


class Memory(Model):
    total = IntType(required=True)
    available = IntType(required=True)


class WorkerSystemStat(Model):
    cpu = PolyModelType(Cpu, required=True)
    memory = PolyModelType(Memory, required=True)
    created_at = DateTimeType(required=False)


class WorkerSystemStatController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate(schema=WorkerSystemStat)
    async def handle(self, request):
        await self.usecase.perform(
            worker_id=request.peer,
            system_stat=request.validated
        )
