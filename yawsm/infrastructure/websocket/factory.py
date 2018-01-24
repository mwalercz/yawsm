from autobahn.asyncio import WebSocketServerFactory


class DqBrokerFactory(WebSocketServerFactory):
    def __init__(self, url, loop):
        WebSocketServerFactory.__init__(self, url, loop=loop)
