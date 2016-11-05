import os
from autobahn.asyncio import WebSocketClientProtocol
from ws_dist_queue.message import WorkerCreatedMessage


class WorkerProtocol(WebSocketClientProtocol):
    API_KEY = '111'

    def onOpen(self):
        print("my pid: {}".format(os.getpid()))
        self.factory.controller.master = self
        headers = {
            'api_key': self.factory.conf.API_KEY
        }
        self.factory.message_sender.send(
            recipient=self.factory.controller.master,
            message_body=WorkerCreatedMessage(),
            message_headers=headers,
        )

    def onMessage(self, payload, isBinary):
        whole_message = self.factory.deserializer.deserialize(payload)

        message_body = whole_message['body']
        headers = whole_message['headers']
        message_type = headers['message_type']

        self.factory.message_sender.update_cookie(headers['cookie'])
        method = self.factory.dispatcher.find_method(message_type)
        method(message=message_body)

    def onClose(self, wasClean, code, reason):
        print('Reason: {}, code: {}'.format(reason, code))
        # reactor.stop()

    def onPing(self, payload):
        self.pingsReceived += 1
        print("Ping received from {} - {}".format(self.peer, self.pingsReceived))
        self.sendPong(payload)
        self.pongsSent += 1
        print("Pong sent to {} - {}".format(self.peer, self.pongsSent))


