from aiohttp import web
from aiohttp_session import get_session

from yawsm.infrastructure.auth.permits import users_must_match, auth_required
from yawsm.infrastructure.http.validator import validate
from yawsm.user.model import User
from yawsm.work.actions.new.usecase import NewWorkUsecase
from yawsm.work.actions.dtos import NewWorkDto


class NewWorkController:
    def __init__(self, usecase: NewWorkUsecase):
        self.usecase = usecase

    @auth_required
    async def handle(self, request):
        data = await request.json()
        session = await get_session(request)
        validated_work = validate(data, schema=NewWorkDto)
        user = User.from_session(session)
        work_id = await self.usecase.perform(
            new_work=validated_work,
            user=user,
        )
        return web.json_response(
            {
                'status': 'ok',
                'work_id': work_id
            }
        )
