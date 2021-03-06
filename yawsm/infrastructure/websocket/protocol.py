import logging

from autobahn.asyncio import WebSocketServerProtocol
from autobahn.websocket import ConnectionDeny

from yawsm.infrastructure.exceptions import (
    AuthenticationFailed, ValidationError,
)
from yawsm.infrastructure.utils import clear_passwords_from_message
from yawsm.infrastructure.websocket.message import IncomingMessage

log = logging.getLogger(__name__)


class DqBrokerProtocol(WebSocketServerProtocol):
    deserializer = NotImplemented
    auth = NotImplemented
    supervisor = NotImplemented

    async def onConnect(self, request):
        try:
            log.info('New connection is being established. %s', request)
            await self.auth.authenticate(headers=request.headers)
            log.info('New connection is opened and authenticated %s', request)
            return None
        except AuthenticationFailed as e:
            log.info(
                'Failed to authenticate connection. %s. Reason: %s',
                request, e.args
            )
            raise ConnectionDeny(code=403, reason=e.args)

    async def onClose(self, wasClean, code, reason):
        log.info('Connection was closed. Reason: %s, peer: %s', reason, self.peer)
        await self.supervisor.handle_message(
            sender=self,
            peer=self.peer,
            message=IncomingMessage(
                path='worker_disconnected'
            ),
        )

    async def onMessage(self, payload, isBinary):
        try:
            raw_message = self.deserializer.deserialize(payload)
            log.info('New message: %s from: %s', clear_passwords_from_message(raw_message), self.peer)
            message = IncomingMessage.from_raw(raw_message)
        except ValidationError as exc:
            log.exception(exc)
            self.sendClose(code=3400, reason=exc.data)
        except Exception as exc:
            log.exception(exc)
            self.sendClose(code=3400, reason='Message is not in json _format')
        else:
            await self.supervisor.handle_message(
                sender=self,
                peer=self.peer,
                message=message,
            )

    async def onPong(self, payload):
        log.debug('pong from %s', self.peer)
