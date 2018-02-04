import argparse
import logging.config

import asyncio
import signal

import functools
import os
import time

import txaio
from autobahn.websocket.util import parse_url
from knot import Container
from peewee import OperationalError

from definitions import ROOT_DIR
from yawsm.dependencies.infrastructure.db import \
    connect_to_db_and_create_tables, create_default_admin_if_not_present
from yawsm.dependencies.app import register_all
from yawsm.work.model import NON_FINAL_STATUSES, WorkStatus


def run_app(
        config_path='yawsm/conf/develop.cfg',
        logging_config_path='yawsm/conf/logging/develop.cfg'
):
    logging.config.fileConfig(logging_config_path)
    # txaio.start_logging(level='debug')
    c = Container(dict(
        config_path=config_path,
    ))
    log = logging.getLogger(__name__)
    register_all(c)
    # txaio.use_asyncio()
    # txaio.config.loop = c('loop')
    try_to_connect_to_db_and_create_admin_if_not_present(
        log, c('conf')['admin']['default_username']
    )

    log.info('changing unfinished work status to UNKNOWN...')
    move_unfinished_works_to_unknown_status(c)

    asyncio.ensure_future(
        c('consumer').consume_all(), loop=c('loop')
    )
    log.info('task queue consumer started..')

    asyncio.ensure_future(make_http_app(c), loop=c('loop'))
    log.info('http started...')

    asyncio.ensure_future(make_ws_app(c), loop=c('loop'))
    log.info('websocket started..')

    for signame in ('SIGINT', 'SIGTERM'):
        c('loop').add_signal_handler(
            getattr(signal, signame),
            functools.partial(exit, signame, c)
        )

    c('loop').run_forever()


def move_unfinished_works_to_unknown_status(c):
    coro = c('actions.work.change_status').perform(
        from_statuses=NON_FINAL_STATUSES - {WorkStatus.UNKNOWN.name},
        to_status=WorkStatus.UNKNOWN.name,
        reason='master_shutdown',
    )
    c('loop').run_until_complete(coro)


def try_to_connect_to_db_and_create_admin_if_not_present(log, default_admin_username):
    while True:
        try:
            connect_to_db_and_create_tables()
            create_default_admin_if_not_present(default_admin_username, log)
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


def exit(signame, c):
    print('Exiting...')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    c('loop').stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='config_path', default='develop.cfg')
    parser.add_argument('-l', dest='logging_config_path', default='develop.cfg')
    args = parser.parse_args()
    run_app(
        config_path=os.path.join(ROOT_DIR, 'yawsm', 'conf', args.config_path),
        logging_config_path=os.path.join(
            ROOT_DIR, 'yawsm', 'conf', 'logging', args.logging_config_path
        ),
    )


if __name__ == '__main__':
    main()
