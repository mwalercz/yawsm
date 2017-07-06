import logging
import logging.config

from knot import Container

from ws_dist_queue.master.dependencies.app import register_app


def make_app(config_path):
    logging.config.fileConfig(config_path)
    # logging.basicConfig(level=10)
    # txaio.start_logging()
    c = Container(dict(
        config_path=config_path,
    ))
    register_app(c)

    return MasterApp(
        host=c('conf')['master']['host'],
        port=c('conf')['master']['port'],
        loop=c('loop'),
        secure_context=c('secure_context'),
        factory=c('factory'),
    )


class MasterApp:
    def __init__(self, loop, host, port, secure_context, factory):
        self.loop = loop
        self.host = host
        self.port = port
        self.secure_context = secure_context
        self.factory = factory
        self.log = logging.getLogger(__name__)

    def run(self):
        coro = self.loop.create_server(
            protocol_factory=self.factory,
            host=self.host,
            port=self.port,
            ssl=self.secure_context
        )
        server = self.loop.run_until_complete(coro)
        try:
            self.log.info('Master app starting...')
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
            self.loop.close()
            self.log.info('Master app closed...')

if __name__ == '__main__':
    app = make_app(config_path='conf/develop.ini')
    app.run()
