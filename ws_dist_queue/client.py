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
import os

from twisted.internet import reactor
from twisted.python import log

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS


class PingClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        print("my pid: {}".format(os.getpid()))
        auth_message = {
            'type': 'auth',
            'parent_pid': os.getppid(),
            'username': 'test',
            'password': 'test123',
        }
        payload = json.dumps(auth_message).encode('utf8')
        self.sendMessage(payload)

    def onMessage(self, payload, isBinary):
        message = json.loads(payload.decode('utf8'))
        print(str(message))
        if message['type'] == 'user_authorized':
            cookie = message['cookie']
            job_message = {
                'type': 'new_job',
                'cookie': cookie,
                'command': 'ls',
                'cwd': '/home/mwal',
            }
            payload = json.dumps(job_message).encode('utf8')
            self.sendMessage(payload)

    def onClose(self, wasClean, code, reason):
        print('Reason: {}, code: {}'.format(reason, code))
        reactor.stop()

    def onPing(self, payload):
        self.pingsReceived += 1
        print("Ping received from {} - {}".format(self.peer, self.pingsReceived))
        self.sendPong(payload)
        self.pongsSent += 1
        print("Pong sent to {} - {}".format(self.peer, self.pongsSent))


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    if len(sys.argv) < 2:
        print("Need the WebSocket server address, i.e. ws://127.0.0.1:9000")
        sys.exit(1)

    factory = WebSocketClientFactory(sys.argv[1])
    factory.protocol = PingClientProtocol
    connectWS(factory)

    reactor.run()
