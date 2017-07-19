import argparse
import logging.config

import asyncio

import os
from autobahn.websocket.util import parse_url
from knot import Container

from definitions import ROOT_DIR
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='config_path', default='develop.ini')
    parser.add_argument('-l', dest='logging_config_path', default='develop.ini')
    args = parser.parse_args()
    run_app(
        config_path=os.path.join(ROOT_DIR, 'dq_broker/conf', args.config_path),
        logging_config_path=os.path.join(
            ROOT_DIR, 'dq_broker/conf/logging', args.logging_config_path
        ),
    )


if __name__ == '__main__':
    main()
