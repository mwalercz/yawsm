import logging

from autobahn.asyncio import WebSocketServerProtocol
from autobahn.websocket import ConnectionDeny

from ws_dist_queue.master.exceptions import AuthenticationFailed, RoleNotFound
from ws_dist_queue.master.infrastructure.auth.base import Role

log = logging.getLogger(__name__)


class Request:
    def __init__(self, message, sender):
        self.message = message
        self.sender = sender


class MasterProtocol(WebSocketServerProtocol):
    deserializer = NotImplemented
    auth = NotImplemented
    router = NotImplemented
    task_scheduler = NotImplemented

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
        log.info('New connection is opened and authenticated %s', request)
        return None, headers

    def onClose(self, wasClean, code, reason):
        log.info(
            'Connection was closed. Reason: %s, peer: %s', reason, self.peer
        )
        try:
            role = self.auth.get_role(self.peer)
        except RoleNotFound:
            return
        controller, responder = self.router.find_responder(
            path=role + '/' + 'down')
        self.task_scheduler.schedule_task(responder, self)
        self.auth.process_remove_worker(self.peer)

    def onMessage(self, payload, isBinary):
        try:
            message = self.deserializer.deserialize(payload)
        except Exception:
            self.sendClose(code=2404, reason='Message is not in json format')
            return
        log.info('New message: %s from: %s', message, self.peer)
        route = self.router.get_route(message['path'])
        if not Role.match(route.role, self.auth.get_role(self.peer)):
            self.sendClose(
                code=2403,
                reason='Not authorized to access this method')
            return
        request = Request(sender=self, message=message)
        self.task_scheduler.schedule_task(route.handler, request)
