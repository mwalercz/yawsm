class WorkerRequestsWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    def handle(self, req):
        self.usecase.perform(worker_id=req.sender.peer)
