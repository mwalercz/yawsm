from aiohttp import web

from infrastructure.auth.permits import users_must_match
from infrastructure.http.controllers.schema import UsernameSchema
from infrastructure.http.validator import validate


class ListWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    @users_must_match
    async def handle(self, request):
        validated = validate(
            {'username': request.match_info.get('username')},
            schema=UsernameSchema
        )

        result = await self.usecase.perform(
            username=validated.username
        )
        return web.json_response(result)
