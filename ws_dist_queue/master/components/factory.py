from autobahn.asyncio import WebSocketServerFactory


class MasterFactory(WebSocketServerFactory):
    def __init__(self, uri):
        WebSocketServerFactory.__init__(self, uri)