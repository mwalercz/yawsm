from ws_dist_queue.master.domain.exceptions import WorkNotFound
from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import WorkIdSchema


class WorkDetailsController:
    def __init__(self, user_auth, usecase, user_client):
        self.user_auth = user_auth
        self.usecase = usecase
        self.user_client = user_client

    @validate(schema=WorkIdSchema)
    async def handle(self, req):
        credentials = self.user_auth.get_credentials(req.sender.peer)
        work_id = req.validated.work_id
        try:
            result = await self.usecase.perform(work_id, credentials.username)
        except WorkNotFound as exc:
            result = {'status': 'work_with_given_work_id_and_username_not_found'}
        self.user_client.send(
            recipient=req.sender,
            message=result,
        )