import logging
import traceback

from dq_broker.infrastructure.exceptions import ValidationError, AccessForbidden
from dq_broker.infrastructure.websocket.request import Request, Response

log = logging.getLogger(__name__)


class Supervisor:
    def __init__(self, response_client, router):
        self.response_client = response_client
        self.router = router

    async def handle_message(self, sender, peer, message):
        request = Request(
            message=message,
            sender=sender,
            peer=peer
        )
        response = await self.handle_request_and_catch_exceptions(request)
        if response:
            self.response_client.send(
                recipient=sender,
                response=response
            )

    async def handle_request_and_catch_exceptions(self, request):
        try:
            route = self.router.get_route(request.message.path)
            return await route.handler(request)
        except AccessForbidden as exc:
            log.exception(exc)
            return Response(
                path=request.message.path,
                status_code=403,
                body={'error': exc.data}
            )
        except ValidationError as exc:
            log.exception(exc)
            return Response(
                path=request.message.path,
                status_code=400,
                body={'error': exc.data},
            )
        except Exception as exc:
            log.exception('Error while handling request: %s', exc)
            return Response(
                path=request.message.path,
                status_code=500,
                body={'error': traceback.format_exc(50)}
            )
