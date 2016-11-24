import logging

import os
from autobahn.asyncio import WebSocketClientProtocol
from ws_dist_queue.messages import Message


class WorkerProtocol(WebSocketClientProtocol):
    log = logging.getLogger(__name__)

    def onOpen(self):
        self.log.info("my pid: {}".format(os.getpid()))
        self.factory.controller.master = self
        headers = {
            'api_key': self.factory.conf.API_KEY
        }
        self.factory.message_sender.send(
            recipient=self.factory.controller.master,
            message_type=Message.worker_created,
            message_headers=headers,
        )

    def onMessage(self, payload, isBinary):
        self.log.info('Message was received: {message}'.format(message=payload))
        whole_message = self.factory.deserializer.deserialize(payload)
        message_body = whole_message['body']
        headers = whole_message['headers']
        message_type = headers['message_type']

        self.factory.message_sender.update_cookie(headers['cookie'])
        method = self.factory.dispatcher.find_method(message_type)
        method(message=message_body)

    def onClose(self, wasClean, code, reason):
        print('Reason: {}, code: {}'.format(reason, code))




