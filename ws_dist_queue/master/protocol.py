from autobahn.asyncio import WebSocketServerProtocol
from twisted.logger import Logger

from ws_dist_queue.model.request import Request


class MasterProtocol(WebSocketServerProtocol):
    log = Logger()

    def onClose(self, wasClean, code, reason):
        self.log.info("connection was closed. Reason {}, peer: {}".format(reason, self.peer))
        self.factory.controller.worker_down(
            req=Request(
                sender=self,
                session=None,
                message=None
            )
        )

    def onMessage(self, payload, isBinary):
        whole_message = self.factory.deserializer.deserialize(payload)
        self.log.info('Message was received: {message!r}', message=payload)

        headers = whole_message['headers']
        message_from = headers['message_from']
        message_type = headers['message_type']
        message_body = whole_message['body']
        cookie = headers.get('cookie')

        if cookie:
            session = self.factory.auth.get_session(
                message_from=message_from,
                cookie=cookie,
            )
            if session:
                self.factory.message_sender.update_cookie(session.cookie)
                self.dispatch_to_method(message_type, message_body, session)
            else:
                self.sendClose(code=3001, reason='Cookie too old or wrong!')
        else:
            session = self.factory.auth.authenticate(headers)
            if session:
                self.factory.message_sender.update_cookie(session.cookie)
                self.dispatch_to_method(message_type, message_body, session)
            else:
                self.sendClose(code=3000, reason='Authentication failed')

    def dispatch_to_method(self, message_type, message_body, session):
        method = self.factory.dispatcher.find_method(message_type)
        method(
            req=Request(
                sender=self,
                session=session,
                message=message_body,
            ),
        )
