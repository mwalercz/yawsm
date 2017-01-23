from autobahn.asyncio import WebSocketClientFactory


class UserFactory(WebSocketClientFactory):
    def __init__(self, master_wss_uri, headers):
        WebSocketClientFactory.__init__(
            self, master_wss_uri, headers=headers
        )
