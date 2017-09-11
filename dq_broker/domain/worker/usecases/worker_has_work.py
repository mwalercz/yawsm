from dq_broker.domain.work.model import WorkEvent, WorkStatus


class WorkerHasWorkUsecase:
    def __init__(self, workers, event_saver):
        self.workers = workers
        self.event_saver = event_saver

    async def perform(self, worker_id, work):
        worker = self.workers.get(worker_id)
        worker.assign(work)
        self.workers.put(worker)
        await self._save_event(worker_id, work)

    async def _save_event(self, worker_id, work):
        await self.event_saver.save_event(
            WorkEvent(
                work_id=work.work_id,
                event_type='worker_has_work',
                work_status=WorkStatus.processing.name,
                context={
                    'worker_id': worker_id,
                }
            )
        )
