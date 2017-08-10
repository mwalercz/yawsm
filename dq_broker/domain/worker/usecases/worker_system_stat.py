class WorkerSystemStatUsecase:
    def __init__(self, workers_repo, current_datetime):
        self.workers_repo = workers_repo
        self.current_datetime = current_datetime

    async def perform(self, worker_id, system_stat):
        system_stat.created_at = self.current_datetime()
        worker = self.workers_repo.get(worker_id)
        worker.append_system_stat(system_stat)
        self.workers_repo.put(worker)
