from autobahn.twisted import WebSocketClientFactory


class UserFactory(WebSocketClientFactory):
    def __init__(
            self, conf, credentials, message, deserializer,
            cookie_keeper, message_sender,
    ):
        WebSocketClientFactory.__init__(self, conf.MASTER_URI)
        self.credentials = credentials
        self.message = message
        self.deserializer = deserializer
        self.cookie_keeper = cookie_keeper
        self.message_sender = message_sender
