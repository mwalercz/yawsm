from aiohttp import web
from aiohttp_session import get_session

from dq_broker.domain.exceptions import WorkNotFound


class WorkDetailsController:
    def __init__(self,  usecase):
        self.usecase = usecase

    async def handle(self, request):
        session = await get_session(request)
        work_id = request.match_info['work_id']
        try:
            result = await self.usecase.perform(
                work_id=work_id,
                username=session['user_info']['username']
            )
            return web.json_response(result)
        except WorkNotFound as exc:
            return web.json_response(
                {'error': 'work_with_given_work_id_and_username_not_found'},
                status=404,
            )
