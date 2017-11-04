import argparse
import logging.config

import asyncio

import os
import time

import txaio
from autobahn.websocket.util import parse_url
from knot import Container
from peewee import OperationalError

from definitions import ROOT_DIR
from dq_broker.dependencies.infrastructure.db import connect_to_db_and_create_tables, create_admin_if_does_not_exist
from dq_broker.dependencies.app import register_all
from dq_broker.work.model import NON_FINAL_STATUSES, WorkStatus


def run_app(
        config_path='dq_broker/conf/develop.ini',
        logging_config_path='dq_broker/conf/logging/develop.ini'
):
    logging.config.fileConfig(logging_config_path)
    txaio.start_logging(level='debug')
    c = Container(dict(
        config_path=config_path,
    ))
    log = logging.getLogger(__name__)
    register_all(c)
    txaio.use_asyncio()
    txaio.config.loop = c('loop')
    try_to_connect_to_db(log)

    log.info('changing unfinished work status to unknown...')
    move_unfinished_works_to_unknown_status(c)

    asyncio.ensure_future(make_http_app(c), loop=c('loop'))
    log.info('http started...')
    asyncio.ensure_future(make_ws_app(c), loop=c('loop'))
    log.info('websocket started..')

    try:
        c('loop').run_forever()
    except KeyboardInterrupt:
        c('loop').close()


def move_unfinished_works_to_unknown_status(c):
    coro = c('actions.work.change_status').perform(
        from_statuses=NON_FINAL_STATUSES,
        to_status=WorkStatus.unknown.name,
        reason='broker_shutdown',
    )
    c('loop').run_until_complete(coro)


def try_to_connect_to_db(log):
    while True:
        try:
            connect_to_db_and_create_tables()
            create_admin_if_does_not_exist()
            break
        except OperationalError as exc:
            log.info('DB is probably unavailable. ' + str(exc))
            time.sleep(1)


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
