from aiohttp import web
from aiohttp_session import get_session

from dq_broker.infrastructure.auth.permits import users_must_match, auth_required
from dq_broker.user.model import User


class ListWorksController:
    def __init__(self, usecase):
        self.usecase = usecase

    @auth_required
    @users_must_match
    async def handle(self, request):
        session = await get_session(request)
        user = User.from_session(session)
        result = await self.usecase.perform(
            user_id=user.user_id
        )
        return web.json_response(result)