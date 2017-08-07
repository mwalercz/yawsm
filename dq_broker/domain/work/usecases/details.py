class WorkDetailsUsecase:
    def __init__(self, work_finder):
        self.work_finder = work_finder

    async def perform(self, work_id, username):
        work = await self.work_finder.find_by_work_id_and_username_with_events(
            work_id, username
        )
        return self._format_work(work)

    def _format_work(self, work):
        return {
            'work_id': work.work_id,
            'command': work.command,
            'cwd': work.cwd,
            'status': work.status,
            'environment': work.env,
            'output': work.output,
            'created_at': work.created_at.isoformat(),
            'events': self._format_events(work.events)
        }

    def _format_events(self, events):
        return [self._format_event(event) for event in events]

    def _format_event(self, event):
        return {
            'event_id': event.event_id,
            'event_type': event.event_type,
            'status': event.status,
            'context': event.context,
            'created_at': event.created_at.isoformat(),
        }