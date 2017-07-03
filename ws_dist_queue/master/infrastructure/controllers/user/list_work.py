from ws_dist_queue.master.infrastructure.request import Response


class ListWorkController:
    def __init__(self, user_auth, usecase):
        self.user_auth = user_auth
        self.usecase = usecase

    async def handle(self, req):
        result = await self.usecase.perform(
            username=self.user_auth.get_username(req.peer)
        )
        return req.get_response(
            body=result,
        )
