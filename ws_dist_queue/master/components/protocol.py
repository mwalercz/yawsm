import asyncio
import inspect
import logging

from autobahn.asyncio import WebSocketServerProtocol
from autobahn.websocket import ConnectionDeny

from ws_dist_queue.master.components.authorization import AuthenticationFailed, RoleNotFound

log = logging.getLogger(__name__)


class Request:
    def __init__(self, message, sender):
        self.message = message
        self.sender = sender


class MasterProtocol(WebSocketServerProtocol):
    deserializer = NotImplemented
    auth = NotImplemented
    router = NotImplemented

    def onConnect(self, request):
        log.info('New connection is being established. %s', request)
        try:
            headers = self.auth.authenticate(request.headers, self.peer) or {}
        except AuthenticationFailed as e:
            log.info(
                'Failed to authenticate connection. %s. Reason: %s',
                request, e.args
            )
            raise ConnectionDeny(code=403, reason='invalid_credentials/cookie')
        else:
            log.info('New connection is opened and authenticated %s', request)
            return None, headers

    def onClose(self, wasClean, code, reason):
        log.info(
            'Connection was closed. Reason: %s, peer: %s', reason, self.peer
        )
        try:
            self.auth.get_role(self.peer)
        except RoleNotFound:
            return
        else:
            role = self.auth.get_role(self.peer)
            controller, responder = self.router.get_responder(path=role + '/' + 'down')
            self.schedule_task(responder, self)
            self.auth.remove(self.peer)

    def onMessage(self, payload, isBinary):
        try:
            message = self.deserializer.deserialize(payload)
        except:
            self.sendClose(code=2404, reason='Message is not in json format')
            return
        log.info('Message was received: %s', message)
        controller, responder = self.router.get_responder(message['path'])
        if controller.ROLE != self.auth.get_role(self.peer):
            self.sendClose(code=2403, reason='Not authorized to access this method')
            return
        request = Request(sender=self, message=message)
        self.schedule_task(responder, request)

    def schedule_task(self, func, arg):
        asyncio.ensure_future(
            self.execute(
                func=func,
                arg=arg,
            )
        )

    async def execute(self, func, arg):
        if inspect.iscoroutinefunction(func):
            await func(arg)
        else:
            func(arg)
