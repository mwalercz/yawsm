import asyncio
import logging
import ssl

from ws_dist_queue.dispatcher import Dispatcher
from ws_dist_queue.master.authorization import AuthService
from ws_dist_queue.master.controller import MasterController, WorkerPicker
from ws_dist_queue.master.factory import MasterFactory
from ws_dist_queue.master.protocol import MasterProtocol
from ws_dist_queue.message import MessageFactory, MASTER_MAPPING
from ws_dist_queue.message_sender import MessageSender, JsonDeserializer


class MasterApp:
    def __init__(self, conf):
        self.conf = conf
        self.secure_context = self.init_context()
        self.loop = asyncio.get_event_loop()
        self.init_logging()
        self.factory = self.init_factory()

    def init_context(self):
        secure_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        secure_context.load_cert_chain(
            self.conf.MASTER_CRT_PATH, self.conf.MASTER_KEY_PATH
        )
        return secure_context

    def init_factory(self):
        factory = MasterFactory(uri=self.conf.MASTER_WSS_URI, **self.init_services())
        factory.protocol = MasterProtocol
        return factory

    def init_logging(self):
        self.loop.set_debug(True)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(name)s  %(message)s')

    def run(self):
        coro = self.loop.create_server(
            protocol_factory=self.factory,
            host=self.conf.MASTER_HOST,
            port=self.conf.MASTER_WSS_PORT,
            ssl=self.secure_context
        )
        server = self.loop.run_until_complete(coro)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
            self.loop.close()

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
