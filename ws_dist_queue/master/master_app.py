import logging

from knot import Container


def make_app(config_path):
    logging.basicConfig(
        level=logging.INFO,
    )
    c = Container(dict(
        config_path=config_path,
    ))
    register(c)

    c('router').register(path='work', controller=c('user_controller'))
    c('router').register(path='worker', controller=c('worker_controller'))

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

    def run(self):
        coro = self.loop.create_server(
            protocol_factory=self.factory,
            host=self.host,
            port=self.port,
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


if __name__ == '__main__':
    app = make_app(config_path='conf/develop.ini')
    app.run()
