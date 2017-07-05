from ws_dist_queue.master.domain.exceptions import WorkNotFound
from ws_dist_queue.master.infrastructure.services.request import validate
from ws_dist_queue.master.schema import WorkIdSchema


class WorkDetailsController:
    def __init__(self, user_auth, usecase):
        self.user_auth = user_auth
        self.usecase = usecase

    @validate(schema=WorkIdSchema)
    async def handle(self, req):
        try:
            result = await self.usecase.perform(
                work_id=req.validated.work_id,
                username=self.user_auth.get_username(req.peer)
            )
            return req.get_response(
                body=result
            )
        except WorkNotFound as exc:
            return req.get_response(
                status_code=404,
                body={'error': 'work_with_given_work_id_and_username_not_found'}
            )