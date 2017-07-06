import logging
import ssl

from knot import Container

from ws_dist_queue.user.dependencies import register


def make_app(config_path, username, password):
    logging.basicConfig(
        level=logging.INFO,
    )
    c = Container(dict(
        config_path=config_path,
        username=username,
        password=password,
    ))

    register(c)
    return UserApp(
        host=c('conf')['master']['host'],
        port=c('conf')['master']['port'],
        loop=c('loop'),
        factory=c('factory'),
    )


class UserApp:
    container = {}

    def __init__(self, host, port, loop, factory):
        self.host = host
        self.port = port
        self.loop = loop
        self.factory = factory

    def send_and_wait(self, path, body=None):
        self.factory.protocol.path = path
        self.factory.protocol.body = body

        coro = self.loop.create_connection(
            protocol_factory=self.factory,
            host=self.host,
            port=self.port,
            ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23)
        )
        self.loop.run_until_complete(coro)
        self.loop.run_forever()


if __name__ == '__main__':
    app = make_app('conf/develop.ini', 'mal', 'matrix')
    app.send_and_wait(
        path='work/new_work',
        body={
            'command': 'ls',
            'cwd': 'haha',
        },
    )
