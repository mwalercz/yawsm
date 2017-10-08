from aiohttp import web
from aiohttp_session import get_session

from dq_broker.exceptions import WorkNotFound
from dq_broker.infrastructure.auth.permits import users_must_match, auth_required
from dq_broker.infrastructure.http.validator import validate
from dq_broker.user.model import User
from dq_broker.work.actions.details.usecase import WorkDetailsUsecase
from dq_broker.worker.actions.dtos import WorkIdDto


class WorkDetailsController:
    def __init__(self,  usecase: WorkDetailsUsecase):
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
        except WorkNotFound as exc:
            return web.json_response(
                {'error': 'work_with_given_work_id_and_username_not_found'},
                status=404,
            )
