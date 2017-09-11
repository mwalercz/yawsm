from aiohttp import web

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.infrastructure.auth.permits import auth_required, admin_only


class WorkerDetailsController:
    def __init__(self, usecase):
        self.usecase = usecase

    @auth_required
    @admin_only
    async def handle(self, request):
        worker_socket = request.match_info['worker_socket']
        try:
            result = await self.usecase.perform(
                worker_socket=worker_socket
            )
            return web.json_response(result)
        except WorkerNotFound:
            return web.json_response(
                {'error': 'worker not found {}'.format(worker_socket)},
                status=404,
            )
