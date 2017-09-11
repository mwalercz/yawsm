class WorkerSystemStatUsecase:
    def __init__(self, workers, current_datetime):
        self.workers = workers
        self.current_datetime = current_datetime

    async def perform(self, worker_socket, system_stat):
        system_stat.created_at = self.current_datetime()
        worker = self.workers.get(worker_socket)
        worker.append_system_stat(system_stat)
        self.workers.put(worker)
