class WorkersNotifier:
    def __init__(self, work_queue, workers, worker_client, picker):
        self.work_queue = work_queue
        self.workers = workers
        self.worker_client = worker_client
        self.picker = picker

    async def notify(self):
        if self.work_queue.empty:
            return
        workers = self.workers.get_free_workers()
        best_workers = await self.picker.pick_best(workers)
        for worker in best_workers:
            self.worker_client.send(
                recipient=worker.worker_ref,
                action_name='work_is_ready'
            )
