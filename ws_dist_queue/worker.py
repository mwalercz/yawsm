import json

import os
from autobahn.twisted import WebSocketClientProtocol

from ws_dist_queue.model.work import Work


class PingClientProtocol(WebSocketClientProtocol):
    API_KEY = '111'

    def onOpen(self):
        print("my pid: {}".format(os.getpid()))
        worker_up_message = {
            'message_type': 'worker_up',
            'api_key': self.API_KEY,
        }
        payload = json.dumps(worker_up_message).encode('utf8')
        self.sendMessage(payload)

    def onMessage(self, payload, isBinary):
        message = json.loads(payload.decode('utf8'))
        print(str(message))
        if message['message_type'] == 'new_job':
            job = Work(**message['job'])

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
