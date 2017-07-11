from aiohttp import web
from aiohttp_session import get_session

from dq_broker.domain.exceptions import WorkerNotFound


class KillWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    async def handle(self, request):
        session = await get_session(request)
        try:
            result = await self.usecase.perform(
                work_id=request.match_info['work_id'],
                username=session['user_info']['username'],
            )
            return web.json_response(result)
        except WorkerNotFound:
            return web.json_response(
                {'error': 'work_found_in_db_but_not_in_memory'},
                status=404,
            )
