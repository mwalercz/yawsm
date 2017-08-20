from aiohttp import web
from aiohttp_session import get_session

from dq_broker.domain.user.model import User
from dq_broker.domain.work.usecases.new import NewWorkUsecase
from dq_broker.infrastructure.auth.permits import users_must_match, auth_required
from dq_broker.infrastructure.http.controllers.schema import NewWorkDto
from dq_broker.infrastructure.http.validator import validate


class NewWorkController:
    def __init__(self, usecase: NewWorkUsecase):
        self.usecase = usecase

    @auth_required
    @users_must_match
    async def handle(self, request):
        data = await request.json()
        session = await get_session(request)
        validated_work = validate(data, schema=NewWorkDto)
        user = User.from_dict(session['user'])
        work_id = await self.usecase.perform(
            new_work=validated_work,
            user=user,
        )
        return web.json_response(
            {'work_id': work_id},
            status=202
        )
