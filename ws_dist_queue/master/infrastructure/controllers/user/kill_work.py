from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import WorkIdSchema


class KillWorkController:
    def __init__(self, user_auth, usecase, user_client):
        self.user_auth = user_auth
        self.usecase = usecase
        self.user_client = user_client

    @validate(schema=WorkIdSchema)
    async def handle(self, req):
        work_id = req.validated.work_id
        credentials = self.user_auth.get_credentials(req.sender.peer)
        result = await self.usecase.perform(work_id, credentials.username)
        self.user_client.send(
            recipient=req.sender,
            message=result,
        )