class NewWorkUsecase:
    def __init__(self, work_queue, workers_notifier, work_saver):
        self.work_queue = work_queue
        self.workers_notifier = workers_notifier
        self.work_saver = work_saver

    async def perform(self, work):
        work_id = await self.work_saver.save_new(work)
        work.set_id(work_id)
        self.work_queue.put(work)
        await self.workers_notifier.notify()
        return work_id
