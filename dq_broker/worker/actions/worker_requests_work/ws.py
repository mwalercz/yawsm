class WorkerRequestsWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    async def handle(self, request):
        await self.usecase.perform(worker_socket=request.peer)
