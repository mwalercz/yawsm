import logging
import traceback

import asyncio

from dq_broker.exceptions import ValidationError, AccessForbidden
from dq_broker.infrastructure.websocket.request import Request, Response

log = logging.getLogger(__name__)


class Supervisor:
    def __init__(self, response_client, router):
        self.response_client = response_client
        self.router = router

    async def handle_message(self, sender, peer, message):
        response = await self.handle_message_and_catch_exceptions(
            peer=peer,
            sender=sender,
            message=message
        )
        if response:
            self.response_client.send(
                recipient=sender,
                response=response
            )

    async def handle_message_and_catch_exceptions(self, sender, peer, message):
        try:
            route = self.router.get_route(message.path)
            request = Request(
                message=message,
                sender=sender,
                peer=peer
            )
            return await asyncio.ensure_future(route.handler(request))
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
                body={'error': traceback.format_exc(50)}
            )