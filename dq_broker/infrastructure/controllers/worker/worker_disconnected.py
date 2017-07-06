class WorkerDisconnectedController:
    def __init__(self, usecase):
        self.usecase = usecase

    async def handle(self, req):
        await self.usecase.perform(worker_id=req.peer)
