from aiohttp import web

from dq_broker.domain.exceptions import WorkNotFound
from dq_broker.infrastructure.auth.permits import users_must_match
from dq_broker.infrastructure.http.controllers.schema import WorkDetailsSchema
from dq_broker.infrastructure.http.validator import validate


class WorkDetailsController:
    def __init__(self,  usecase):
        self.usecase = usecase

    @users_must_match
    async def handle(self, request):
        validated = validate(
            {
                'work_id': request.match_info.get('work_id'),
                'username': request.match_info.get('username'),
            },
            schema=WorkDetailsSchema
        )
        try:
            result = await self.usecase.perform(
                work_id=validated.work_id,
                username=validated.username,
            )
            return web.json_response(result)
        except WorkNotFound as exc:
            return web.json_response(
                {'error': 'work_with_given_work_id_and_username_not_found'},
                status=404,
            )
