import logging

from autobahn.asyncio import WebSocketServerProtocol
from autobahn.websocket import ConnectionDeny

from ws_dist_queue.master.exceptions import (
    AuthenticationFailed, ValidationError,
    SessionNotFound
)
from ws_dist_queue.master.infrastructure.auth.base import Role
from ws_dist_queue.master.infrastructure.message import IncomingMessage

log = logging.getLogger(__name__)


class MasterProtocol(WebSocketServerProtocol):
    deserializer = NotImplemented
    auth = NotImplemented
    supervisor = NotImplemented

    def onConnect(self, request):
        try:
            log.info('New connection is being established. %s', request)
            self.auth.authenticate(peer=self.peer, headers=request.headers)
            headers = self.auth.get_headers(self.peer)
            log.info('New connection is opened and authenticated %s', request)
            return None, headers
        except AuthenticationFailed as e:
            log.info(
                'Failed to authenticate connection. %s. Reason: %s',
                request, e.args
            )
            raise ConnectionDeny(code=403, reason='invalid_credentials/cookie')

    async def onClose(self, wasClean, code, reason):
        try:
            log.info('Connection was closed. Reason: %s, peer: %s', reason, self.peer)
            if Role.worker == self.auth.get_role(self.peer):
                await self.supervisor.handle_message(
                    sender=self,
                    peer=self.peer,
                    message=IncomingMessage(
                        path='worker_disconnected'
                    ),
                )

            self.auth.remove(self.peer)
        except SessionNotFound as exc:
            log.exception(exc)

    async def onMessage(self, payload, isBinary):
        try:
            raw_message = self.deserializer.deserialize(payload)
            log.info('New message: %s from: %s', raw_message, self.peer)
            message = IncomingMessage.from_raw(raw_message)
        except ValidationError as exc:
            log.exception(exc)
            self.sendClose(code=2400, reason=exc.data)
        except Exception as exc:
            log.exception(exc)
            self.sendClose(code=2400, reason='Message is not in json format')
        else:
            await self.supervisor.handle_message(
                sender=self,
                peer=self.peer,
                message=message,
            )
