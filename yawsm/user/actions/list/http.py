from aiohttp import web

from yawsm.infrastructure.auth.permits import auth_required, admin_only
from .usecase import ListUserUsecase


class ListUserController:
    def __init__(self, usecase: ListUserUsecase):
        self.usecase = usecase

    @auth_required
    @admin_only
    async def handle(self, request):
        result = await self.usecase.perform()
        return web.json_response(result)
