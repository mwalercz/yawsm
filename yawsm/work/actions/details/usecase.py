from yawsm.infrastructure.db.work import Work
from yawsm.infrastructure.repositories.work import WorkFinder


class WorkDetailsUsecase:
    def __init__(self, work_finder: WorkFinder):
        self.work_finder = work_finder

    async def perform(self, work_id, user_id):
        work = await self.work_finder.find_by_work_id_and_user_id_with_events(
            work_id, user_id
        )
        return self._format_work(work)

    def _format_work(self, work: Work):
        return {
            'work_id': work.work_id,
            'command': work.command,
            'cwd': work.cwd,
            'status': work.status,
            'environment': work.env,
            'output': work.output,
            'exit_code': work.exit_code,
            'created_at': work.created_at.isoformat(),
            'events': self._format_events(work.events)
        }

    def _format_events(self, events):
        return [self._format_event(event) for event in events]

    def _format_event(self, event):
        return {
            'event_id': event.event_id,
            'reason': event.event_type,
            'status': event.status,
            'context': event.context,
            'created_at': event.created_at.isoformat(),
        }