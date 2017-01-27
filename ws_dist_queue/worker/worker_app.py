import asyncio
import logging
import signal
import ssl

import functools
from knot import Container

from ws_dist_queue.worker.dependencies.container import register


def make_app(config_path):
    logging.basicConfig(
        level=logging.DEBUG,
    )
    c = Container(dict(
        config_path=config_path,
    ))
    register(c)
    return WorkerApp(
        host=c('conf')['master']['host'],
        port=c('conf')['master']['port'],
        factory=c('factory'),
        loop=c('loop'),
        controller=c('worker_controller'),
    )


class WorkerApp:

    def __init__(self, host, port, factory, loop, controller):
        self.host = host
        self.port = port
        self.factory = factory
        self.loop = loop
        self.controller = controller
        self.register_signal_handlers()

    def run(self):
        coro = self.loop.create_connection(
            protocol_factory=self.factory,
            host=self.host,
            port=self.port,
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
        self.controller.clean_up()
        self.loop.stop()


if __name__ == "__main__":
    app = make_app(
        config_path='conf/develop.ini'
    )
    app.run()
