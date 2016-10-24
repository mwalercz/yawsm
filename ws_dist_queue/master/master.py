###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################
import json
import sys

import paramiko
import time
from paramiko import SSHClient
from twisted.internet import reactor, ssl
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS

from autobahn.twisted.resource import WebSocketResource


class PingServerProtocol(WebSocketServerProtocol):
    API_KEY = '111'

    def doPing(self):
        if self.run:
            self.sendPing()
            self.factory.pingsSent[self.peer] += 1
            print("Ping sent to {} - {}".format(self.peer, self.factory.pingsSent[self.peer]))
            # reactor.callLater(10, self.doPing)

    def onPong(self, payload):
        self.factory.pongsReceived[self.peer] += 1
        print("Pong received from {} - {}".format(self.peer, self.factory.pongsReceived[self.peer]))

    def onOpen(self):
        self.factory.register(self)

    def onClose(self, wasClean, code, reason):
        print("connection was closed. Reason {}, peer: {}".format(reason, self.peer))
        self.factory.unregister(self)

    def onMessage(self, payload, isBinary):
        message = json.loads(payload.decode('utf8'))
        if message['type'] == 'auth':
                cookie = self.factory.auth.authenticate(message)
                if cookie:
                    client_authorized_message = {
                        'type': 'client_authorized',
                        'cookie': cookie,
                    }
                    payload = json.dumps(client_authorized_message).encode('utf8')
                    self.sendMessage(payload)
                else:
                    self.sendClose(code=3000, reason='wrong username or password')
        else:
            session = self.factory.services.auth.get_session(
                message_from=message['from'],
                cookie=message['cookie'],
            )
            if session:
                method = self.factory.dispatcher.find_method(message['type'])
                method(
                    req=Request(
                        message=message,
                        sender=self,
                        session=session,
                    ),
                )
            else:
                self.sendClose(code=3001, reason='u must auth first!')

        elif message['type'] == 'new_job':
            cookie = message['cookie']
            session = self.factory.authenticated_users.get(cookie, None)
            if session:


        elif message['type'] == 'auth_worker':
            pass

class MasterFactory(WebSocketServerFactory):
    def __init__(self, uri, services):
        WebSocketServerFactory.__init__(self, uri)
        self.dispatcher = services['dispatcher']
        self.auth = services['auth_service']
        self.workers = []
        self.clients = []
        self.peers = []
        self.auth =
        self.authenticated_users = {}

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)


class Request:
    def __init__(self, message, session, sender):
        self.message = message
        self.session = session
        self.sender = sender


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    contextFactory = ssl.DefaultOpenSSLContextFactory('../keys/server.key',
                                                      '../keys/server.crt')
    services = {
        'dispatcher': 'dispatcher',
        'auth_service': 'auth_service',
    }
    factory = MasterFactory('wss://127.0.0.1:9000', services)

    factory.protocol = PingServerProtocol
    listenWS(factory, contextFactory)

    resource = WebSocketResource(factory)

    root = File(".")
    # note that Twisted uses bytes for URLs, which mostly affects Python3
    root.putChild('ws', resource)
    site = Site(root)

    reactor.listenSSL(8080, site, contextFactory)
    # reactor.listenTCP(8080, site)

    reactor.run()
