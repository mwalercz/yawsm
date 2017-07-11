from aiohttp import web
from aiohttp_session import get_session


class ListWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    async def handle(self, request):
        session = await get_session(request)
        result = await self.usecase.perform(
            username=session['user_info']['username']
        )
        return web.json_response(result)
