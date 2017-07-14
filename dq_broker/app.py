import logging.config

import asyncio
from autobahn.websocket.util import parse_url
from knot import Container

from dq_broker.dependencies.app import register_all


def run_app(
        config_path='conf/develop.ini',
        logging_config_path='conf/logging/develop.ini'
):
    logging.config.fileConfig(logging_config_path)
    c = Container(dict(
        config_path=config_path,
    ))
    register_all(c)
    log = logging.getLogger(__name__)
    # c('before_startup')()
    asyncio.ensure_future(make_http_app(c), loop=c('loop'))
    log.info('http started...')
    asyncio.ensure_future(make_ws_app(c), loop=c('loop'))
    log.info('websocket started..')

    try:
        c('loop').run_forever()
    except KeyboardInterrupt:
        # c('before_shutdown')()
        c('loop').close()


def make_ws_app(c):
    is_secure, host, port, resource, path, params = (
        parse_url(c('conf')['websocket']['url'])
    )
    return c('loop').create_server(
        protocol_factory=c('factory'),
        host=host,
        port=port,
        ssl=c('secure_context'),
    )


def make_http_app(c):
    return c('loop').create_server(
        protocol_factory=c('http_app').make_handler(),
        host=c('conf')['http']['host'],
        port=c('conf')['http']['port'],
        ssl=c('secure_context'),
    )

if __name__ == '__main__':
    run_app()

