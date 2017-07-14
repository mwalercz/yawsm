from dq_broker.domain.workers.model import Worker


class WorkerConnectedController:
    def __init__(self, usecase):
        self.usecase = usecase

    async def handle(self, request):
        worker = Worker(
            worker_id=request.peer,
            worker_ref=request.sender,
        )
        self.usecase.perform(worker)
