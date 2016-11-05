import os
from autobahn.twisted.websocket import WebSocketClientProtocol
from twisted.internet import reactor


class UserProtocol(WebSocketClientProtocol):
    def onOpen(self):
        credentials = self.factory.credentials
        message = self.factory.message
        cookie = self.factory.cookie_keeper.get_cookie()
        if credentials:
            headers = {
                'username': credentials.username,
                'password': credentials.password,
                'parent_pid': os.getppid()
            }
        elif cookie:
            headers = {
                'cookie': cookie
            }
        else:
            headers = {}
        self.factory.message_sender.send(
            recipient=self,
            message_body=message,
            message_headers=headers,
        )

    def onMessage(self, payload, isBinary):
        raw_message = self.factory.deserializer.deserialize(payload)
        try:
            cookie = raw_message['headers']['cookie']
        except KeyError:
            pass
        else:
            self.factory.cookie_keeper.save(cookie)
        finally:
            body = self.factory.serializer.serialize(raw_message['body'])
            print('received: {}'.format(body))
            self.sendClose(code=3200, reason='OK')

    def onClose(self, wasClean, code, reason):
        print('Reason: {}, code: {}'.format(reason, code))
        reactor.stop()
