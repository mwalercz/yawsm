from aiohttp import web
from aiohttp_session import get_session

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.domain.user.model import User
from dq_broker.domain.work.usecases.kill import KillWorkUsecase
from dq_broker.infrastructure.auth.permits import users_must_match, auth_required
from dq_broker.infrastructure.http.controllers.schema import WorkIdDto
from dq_broker.infrastructure.http.validator import validate


class KillWorkController:
    def __init__(self, usecase: KillWorkUsecase):
        self.usecase = usecase

    @auth_required
    @users_must_match
    async def handle(self, request):
        session = await get_session(request)
        user = User.from_session(session)
        validated = validate(
            {'work_id': request.match_info.get('work_id')},
            schema=WorkIdDto
        )
        try:
            result = await self.usecase.perform(
                work_id=validated.work_id,
                user_id=user.user_id,
            )
            return web.json_response(result)
        except WorkerNotFound:
            return web.json_response(
                {'error': 'work_found_in_db_but_not_in_memory'},
                status=404,
            )
