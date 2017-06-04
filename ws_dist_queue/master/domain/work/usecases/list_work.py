class ListWorkUsecase:
    def __init__(self, work_finder):
        self.work_finder = work_finder

    async def perform(self, username):
        work_list = await self.work_finder.find_by_username(username)
        formatted_work_list = [
            self._format_work(work) for work in work_list
        ]
        return formatted_work_list

    def _format_work(self, work):
        return {
            'work_id': work.work_id,
            'command': work.command,
            'cwd': work.cwd,
            'environment': work.env,
            'output': work.output,
            'created_at': work.created_at,
        }
