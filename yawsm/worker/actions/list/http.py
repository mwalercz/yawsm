from aiohttp import web

from yawsm.infrastructure.auth.permits import auth_required, admin_only


class WorkerListController:
    def __init__(self, usecase):
        self.usecase = usecase

    @auth_required
    @admin_only
    async def handle(self, request):
        result = await self.usecase.perform()
        return web.json_response(result)
