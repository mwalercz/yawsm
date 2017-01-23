from autobahn.asyncio import WebSocketClientFactory


class WorkerFactory(WebSocketClientFactory):
    def __init__(
            self, conf, dispatcher,
            message_sender, controller
    ):
        WebSocketClientFactory.__init__(self, conf.MASTER_WSS_URI)
        self.conf = conf
        self.dispatcher = dispatcher
        self.message_sender = message_sender
        self.controller = controller