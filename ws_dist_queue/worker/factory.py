from autobahn.asyncio import WebSocketClientFactory


class WorkerFactory(WebSocketClientFactory):
    def __init__(
            self, conf, deserializer, dispatcher,
            message_sender, controller
    ):
        WebSocketClientFactory.__init__(self, conf.MASTER_URI)
        self.conf = conf
        self.deserializer = deserializer
        self.dispatcher = dispatcher
        self.message_sender = message_sender
        self.controller = controller