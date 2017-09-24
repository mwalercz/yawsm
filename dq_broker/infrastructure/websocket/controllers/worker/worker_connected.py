from jsonschema import validate
from peewee import Model
from schematics.types import FloatType, IntType, PolyModelType, DateTimeType

from dq_broker.domain.worker.usecases.worker_connected import NewWorkerDto


class Cpu(Model):
    count = IntType(required=True)
    load_15 = FloatType(required=True)


class Memory(Model):
    total = IntType(required=True)
    available = IntType(required=True)


class FullSystemStat(Model):
    cpu = PolyModelType(Cpu, required=True)
    memory = PolyModelType(Memory, required=True)
    created_at = DateTimeType(required=False)


class WorkerConnectedController:
    def __init__(self, usecase):
        self.usecase = usecase

    @validate
    async def handle(self, request):
        worker = NewWorkerDto(
            worker_socket=request.peer,
            worker_ref=request.sender,
        )
        await self.usecase.perform(worker)
