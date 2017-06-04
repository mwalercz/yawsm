import pprint

from autobahn.asyncio import WebSocketClientProtocol


class UserProtocol(WebSocketClientProtocol):
    path = NotImplemented
    body = NotImplemented
    cookie_keeper = NotImplemented
    loop = NotImplemented
    serializer = NotImplemented
    deserializer = NotImplemented

    def onConnect(self, response):
        cookie = response.headers.get('x-cookie')
        if cookie:
            self.cookie_keeper.save_new(cookie)

    def onOpen(self):
        message = {
            'path': self.path,
            'body': self.body,
        }
        serialized_message = self.serializer.serialize(message)
        self.sendMessage(serialized_message)

    def onMessage(self, payload, isBinary):
        message = self.deserializer.deserialize(payload)
        print('MESSAGE: ' + message['info'])
        pprint.PrettyPrinter(indent=4).pprint(message['body'])
        self.sendClose(code=3200, reason='Finished')

    def onClose(self, wasClean, code, reason):
        self.loop.stop()
