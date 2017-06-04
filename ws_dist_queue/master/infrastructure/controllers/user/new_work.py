from ws_dist_queue.master.domain.work.model import CommandData
from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import NewWorkSchema
from ws_dist_queue.master.domain.work.model import Work


class NewWorkController:
    def __init__(self, user_auth, usecase, user_client):
        self.user_auth = user_auth
        self.usecase = usecase
        self.user_client = user_client

    @validate(schema=NewWorkSchema)
    async def handle(self, req):
        credentials = self.user_auth.get_credentials(req.sender.peer)
        new_work = Work.new(
            command_data=CommandData(
                command=req.validated.command,
                env=req.validated.env,
                cwd=req.validated.cwd,
            ),
            credentials=credentials
        )
        await self.usecase.perform(new_work)
        result = {'status': 'work_accepted'}
        self.user_client.send(
            recipient=req.sender,
            message=result,
        )
