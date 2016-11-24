import logging

import asyncio
from autobahn.asyncio import WebSocketServerProtocol
from ws_dist_queue.model.request import Request


class MasterProtocol(WebSocketServerProtocol):
    log = logging.getLogger(__name__)

    async def onClose(self, wasClean, code, reason):
        self.log.info(
            "connection was closed. Reason {}, peer: {}".format(
                reason, self.peer
            )
        )
        await self.factory.controller.worker_down(
            req=Request(
                sender=self,
                session=None,
                message=None
            )
        )

    def onMessage(self, payload, isBinary):
        whole_message = self.factory.deserializer.deserialize(payload)
        self.log.info('Message was received: {message}'.format(message=payload))

        headers = whole_message['headers']
        message_from = headers['message_from']
        message_type = headers['message_type']
        cookie = headers.get('cookie')

        try:
            message_body = self.try_to_get_message_body(message_type, whole_message)
        except Exception as e:
            self.log.warning(e)
            return
        if message_body:
            try:
                message_body.validate()
            except Exception as e:
                self.log.warning(e)
                return

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
        request = Request(sender=self, session=session, message=message_body)
        asyncio.ensure_future(
            self.execute(
                method=method,
                req=request
            )
        )

    async def execute(self, method, req):
        await method(req)

    def try_to_get_message_body(self, message_type, whole_message):
        message_obj = self.factory.message_fact.get_object(message_type)
        raw_message_body = whole_message.get('body', None)
        return message_obj(raw_message_body) if raw_message_body else None
