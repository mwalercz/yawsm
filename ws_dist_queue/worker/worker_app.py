import asyncio
import signal
import ssl

import functools
from ws_dist_queue.dispatcher import Dispatcher
from ws_dist_queue.message_sender import MessageSender, JsonDeserializer
from ws_dist_queue.worker.controller import WorkerController
from ws_dist_queue.worker.factory import WorkerFactory
from ws_dist_queue.worker.protocol import WorkerProtocol


class WorkerApp:
    def __init__(self, conf):
        self.conf = conf
        self.init_logging()
        self.factory = self.init_factory(
            conf=conf,
        )
        self.loop = asyncio.get_event_loop()
        self.factory.controller.loop = self.loop
        self.register_signal_handlers()

    def run(self):
        coro = self.loop.create_connection(
            protocol_factory=self.factory,
            host=self.conf.MASTER_HOST,
            port=self.conf.MASTER_WSS_PORT,
            ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
        )
        self.loop.run_until_complete(coro)
        self.loop.run_forever()
        self.loop.close()

    def register_signal_handlers(self):
        for signame in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(self.clean_up, signame)
            )

    def clean_up(self, signame):
        self.factory.controller.clean_up()
        self.loop.stop()

    def init_factory(self, conf):
        factory = WorkerFactory(
            conf=conf,
            **self.init_services(conf),
        )
        factory.protocol = WorkerProtocol
        return factory

    def init_logging(self):
        pass

    def init_services(self, conf):
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


if __name__ == "__main__":
    import ws_dist_queue.settings.defaults as defaults

    app = WorkerApp(
        conf=defaults,
    )
    app.run()
