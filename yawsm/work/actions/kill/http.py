from aiohttp import web
from aiohttp_session import get_session

from yawsm.exceptions import WorkerNotFound
from yawsm.infrastructure.auth.permits import users_must_match, auth_required
from yawsm.infrastructure.http.validator import validate
from yawsm.user.model import User
from yawsm.work.actions.kill.usecase import KillWorkUsecase
from yawsm.work.model import KillWork
from yawsm.worker.actions.dtos import WorkIdDto


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

