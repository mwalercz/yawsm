from dq_broker.domain.worker.usecases.worker_connected import NewWorkerDto


class WorkerConnectedController:
    def __init__(self, usecase):
        self.usecase = usecase

    async def handle(self, request):
        worker = NewWorkerDto(
            worker_socket=request.peer,
            worker_ref=request.sender,
        )
        await self.usecase.perform(worker)
