from dq_broker.domain.workers.model import Worker


class WorkerConnectedController:
    def __init__(self, usecase):
        self.usecase = usecase

    def handle(self, req):
        worker = Worker(
            worker_id=req.peer,
            worker_ref=req.sender,
        )
        self.usecase.perform(worker)
