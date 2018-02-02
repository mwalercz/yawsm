from aiohttp import web
from aiohttp_session import get_session

from yawsm.infrastructure.auth.permits import users_must_match, auth_required
from yawsm.user.model import User


class ListWorksController:
    def __init__(self, usecase):
        self.usecase = usecase

    @auth_required
    async def handle(self, request):
        session = await get_session(request)
        user = User.from_session(session)
        statuses = request.query.getall('status', None)
        result = await self.usecase.perform(
            user_id=user.user_id,
            statuses=statuses
        )
        return web.json_response(result)
