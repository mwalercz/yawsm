from dq_broker.domain.worker.model import Worker


class WorkerConnectedController:
    def __init__(self, usecase):
        self.usecase = usecase

    async def handle(self, request):
        worker = Worker(
            worker_socket=request.peer,
            worker_ref=request.sender,
        )
        await self.usecase.perform(worker)
