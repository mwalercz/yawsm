import sys

from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor
from twisted.internet import ssl
from twisted.python import log
from ws_dist_queue.dispatcher import Dispatcher
from ws_dist_queue.message_sender import MessageSender, JsonDeserializer
from ws_dist_queue.worker.controller import WorkerController
from ws_dist_queue.worker.factory import WorkerFactory
from ws_dist_queue.worker.protocol import WorkerProtocol


class WorkerApp:
    def __init__(self, conf):
        self.conf = conf
        self.init_logging()
        self.configure_twisted()
        self.factory = self.init_factory()
        self.register_signal_handlers()

    def run(self):
        connectWS(self.factory, ssl.ClientContextFactory())
        reactor.run()

    def register_signal_handlers(self):
        reactor.addSystemEventTrigger('before', 'shutdown', self.clean_up)

    def init_logging(self):
        log.startLogging(sys.stdout)

    def clean_up(self):
        self.factory.controller.clean_up()

    def init_factory(self):
        factory = WorkerFactory(
            conf=self.conf,
            **self.init_services(),
        )
        factory.protocol = WorkerProtocol
        return factory

    def init_services(self):
        message_sender = MessageSender(
            message_from='worker'
        )
        worker_controller = WorkerController(
            message_sender=message_sender,
        )
        worker_dispatcher = Dispatcher(
            controller=worker_controller,
        )
        services = {
            'message_sender': message_sender,
            'deserializer': JsonDeserializer(),
            'controller': worker_controller,
            'dispatcher': worker_dispatcher,
        }
        return services

    def configure_twisted(self):
        reactor.suggestThreadPoolSize(30)


if __name__ == "__main__":
    import ws_dist_queue.settings.defaults as defaults

    app = WorkerApp(
        conf=defaults,
    )
    app.run()
