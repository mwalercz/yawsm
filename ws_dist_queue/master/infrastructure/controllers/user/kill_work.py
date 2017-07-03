from ws_dist_queue.master.domain.exceptions import WorkerNotFound
from ws_dist_queue.master.infrastructure.request import Response
from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import WorkIdSchema


class KillWorkController:
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
        except WorkerNotFound:
            response = req.get_response(
                status_code=404,
                body={'error': 'work_found_in_db_but_not_in_memory'}
            )
            return response
