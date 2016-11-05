from autobahn.twisted import WebSocketClientFactory


class UserFactory(WebSocketClientFactory):
    def __init__(
            self, conf, credentials, message, deserializer,
            cookie_keeper, message_sender, serializer
    ):
        WebSocketClientFactory.__init__(self, conf.MASTER_WSS_URI)
        self.credentials = credentials
        self.message = message
        self.serializer = serializer
        self.deserializer = deserializer
        self.cookie_keeper = cookie_keeper
        self.message_sender = message_sender
