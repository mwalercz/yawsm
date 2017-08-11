from dq_broker.infrastructure.repositories.work import WorkFinder


class ListWorkUsecase:
    def __init__(self, work_finder: WorkFinder):
        self.work_finder = work_finder

    async def perform(self, user_id):
        work_list = await self.work_finder.find_by_user_id(user_id)
        return {
            'works': self._format_work_list(work_list)
        }

    def _format_work(self, work):
        return {
            'work_id': work.work_id,
            'command': work.command,
            'status': work.status,
            'cwd': work.cwd,
            'environment': work.env,
            'output': work.output,
            'created_at': work.created_at.isoformat(),
        }

    def _format_work_list(self, work_list):
        return [
            self._format_work(work) for work in work_list
        ]
