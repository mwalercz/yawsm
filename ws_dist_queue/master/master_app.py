import sys

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import listenWS
from twisted.internet import reactor, ssl
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from ws_dist_queue.dispatcher import Dispatcher
from ws_dist_queue.master.authorization import AuthService
from ws_dist_queue.master.controller import MasterController, WorkerPicker
from ws_dist_queue.master.factory import MasterFactory
from ws_dist_queue.master.message_sender import MessageSender, JsonDeserializer
from ws_dist_queue.master.protocol import MasterProtocol
from ws_dist_queue.message import MessageFactory, MASTER_MAPPING


class MasterApp:
    def __init__(self, conf):
        self.init_logging()
        self.conf = conf
        self.context_factory = self.init_context()
        self.factory = self.init_factory()
        self.site = self.init_site(WebSocketResource(self.factory))

    def init_context(self):
        return ssl.DefaultOpenSSLContextFactory(
            self.conf.MASTER_KEY_PATH, self.conf.MASTER_CRT_PATH
        )

    def init_factory(self):
        factory = MasterFactory(uri=self.conf.MASTER_WSS_URI, **self.init_services())
        factory.setProtocolOptions(
            allowedOrigins=[
                "https://127.0.0.1:8080",
                "https://localhost:8080",
            ]
        )
        factory.protocol = MasterProtocol
        return factory

    def init_site(self, resource):
        root = File(".")
        root.putChild('ws', resource)
        return Site(root)

    def init_logging(self):
        log.startLogging(sys.stdout)

    def run(self):
        listenWS(self.factory, self.context_factory)
        reactor.listenSSL(self.conf.MASTER_WWW_PORT, self.site, self.context_factory)
        reactor.run()

    def init_services(self):
        message_sender = MessageSender(message_from='master')
        worker_picker = WorkerPicker()
        master_controller = MasterController(
            message_sender=message_sender,
            worker_picker=worker_picker
        )
        services = {
            'controller': master_controller,
            'message_factory': MessageFactory(MASTER_MAPPING),
            'dispatcher': Dispatcher(controller=master_controller),
            'auth': AuthService(conf=self.conf),
            'message_sender': message_sender,
            'deserializer': JsonDeserializer()
        }
        return services


if __name__ == '__main__':
    import ws_dist_queue.settings.defaults as defaults
    app = MasterApp(defaults)
    app.run()

