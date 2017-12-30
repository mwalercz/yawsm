from aiohttp import web
from aiohttp_session import get_session

from dq_broker.exceptions import WorkerNotFound
from dq_broker.infrastructure.auth.permits import users_must_match, auth_required
from dq_broker.infrastructure.http.validator import validate
from dq_broker.user.model import User
from dq_broker.work.actions.kill.usecase import KillWorkUsecase
from dq_broker.work.model import KillWork
from dq_broker.worker.actions.dtos import WorkIdDto


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
        result = await self.usecase.perform(
            KillWork(
                work_id=validated.work_id,
                user_id=user.user_id,
            )
        )
        return web.json_response(result)

