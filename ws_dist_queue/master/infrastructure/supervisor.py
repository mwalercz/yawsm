import logging

from ws_dist_queue.master.exceptions import ValidationError, AccessForbidden
from ws_dist_queue.master.infrastructure.request import Request, Response

log = logging.getLogger(__name__)


class Supervisor:
    def __init__(self, executor, response_client, router):
        self.executor = executor
        self.response_client = response_client
        self.router = router

    async def handle_message(self, sender, peer, message):
        response = await self._handle_message_and_catch_exceptions(
            peer=peer,
            sender=sender,
            message=message,
        )
        if response:
            self.response_client.send(
                recipient=sender,
                response=response,
            )

    async def _handle_message_and_catch_exceptions(self, sender, peer, message):
        try:
            route = self.router.get_route(message.path, peer)
            request = Request(
                sender=sender,
                message=message,
                peer=peer,
                route=route,
            )
            return await self._execute_request(
                request=request,
                route=route
            )
        except AccessForbidden as exc:
            log.exception(exc)
            return Response(
                path=message.path,
                status_code=403,
                body={'error': exc.data}
            )
        except ValidationError as exc:
            log.exception(exc)
            return Response(
                path=message.path,
                status_code=400,
                body={'error': exc.data},
            )
        except Exception as exc:
            log.exception('Error while handling request: %s', exc)
            return Response(
                path=message.path,
                status_code=500,
            )

    async def _execute_request(self, request, route):
        return await self.executor.execute(
            func=route.handler, arg=request
        )
