from autobahn.asyncio import WebSocketServerFactory


class MasterFactory(WebSocketServerFactory):
    def __init__(
            self, uri, deserializer, dispatcher, auth,
            message_sender, message_factory, controller
    ):
        WebSocketServerFactory.__init__(self, uri)
        self.deserializer = deserializer
        self.dispatcher = dispatcher
        self.auth = auth
        self.message_sender = message_sender
        self.message_fact = message_factory
        self.controller = controller