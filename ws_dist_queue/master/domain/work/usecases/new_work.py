class NewWorkUsecase:
    def __init__(self, work_queue, workers_notifier, work_repo):
        self.work_queue = work_queue
        self.workers_notifier = workers_notifier
        self.work_repo = work_repo

    async def perform(self, work):
        await self.work_repo.save_new(work)
        self.work_queue.put(work)
        self.workers_notifier.notify()
