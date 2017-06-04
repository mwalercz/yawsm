class WorkersNotifier:
    ACTION_NAME = 'work_is_ready'

    def __init__(self, work_queue, workers_repo, worker_client, picker):
        self.work_queue = work_queue
        self.workers_repo = workers_repo
        self.worker_client = worker_client
        self.picker = picker

    def notify(self):
        if self.work_queue.empty:
            return
        best_workers = self.picker.pick_best(self.workers_repo.free_workers)
        for worker in best_workers:
            self.worker_client.send(
                recipient=worker.worker_ref,
                action_name=self.ACTION_NAME
            )
