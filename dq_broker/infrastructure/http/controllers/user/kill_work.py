from aiohttp import web

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.infrastructure.auth.permits import users_must_match, auth_required
from dq_broker.infrastructure.http.controllers.schema import WorkDetailsSchema
from dq_broker.infrastructure.http.validator import validate


class KillWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    @auth_required
    @users_must_match
    async def handle(self, request):
        validated = validate(
            {
                'work_id': request.match_info.get('work_id'),
                'username': request.match_info.get('username')
            },
            schema=WorkDetailsSchema
        )
        try:
            result = await self.usecase.perform(
                work_id=validated.work_id,
                username=validated.username,
            )
            return web.json_response(result)
        except WorkerNotFound:
            return web.json_response(
                {'error': 'work_found_in_db_but_not_in_memory'},
                status=404,
            )
