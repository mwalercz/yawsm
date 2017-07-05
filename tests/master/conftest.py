from configparser import ConfigParser

import asyncio
from unittest.mock import sentinel

import os
import pytest
from peewee_async import Manager

from definitions import ROOT_DIR
from ws_dist_queue.master.domain.work.model import Work, CommandData
from ws_dist_queue.master.domain.workers.model import Worker
from ws_dist_queue.master.infrastructure.auth.user import Credentials
from ws_dist_queue.master.infrastructure.db.work import database
from ws_dist_queue.master.infrastructure import db


def pytest_addoption(parser):
    parser.addoption(
        "--settings", action="store",
        default="develop.ini", help="config name"
    )


@pytest.fixture
def conf_path(request):
    conf_name = request.config.getoption("--settings")
    conf_path = os.path.join(ROOT_DIR, 'ws_dist_queue/master/conf/', conf_name)
    return conf_path


@pytest.fixture
def fixt_conf(conf_path):
    conf = ConfigParser()
    conf.read(conf_path)
    return conf


@pytest.fixture
def fixt_db(fixt_conf):
    database.init(**fixt_conf['db'])
    db.work.Work.create_table(True)
    db.work.WorkEvent.create_table(True)
    database.set_autocommit(False)
    return database


@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def fixt_objects(fixt_db, event_loop):
    objects = Manager(database=fixt_db, loop=event_loop)
    return objects


@pytest.fixture
def fixt_work(fixt_command_data, fixt_credentials):
    return Work.new(fixt_command_data, fixt_credentials)


@pytest.fixture
def fixt_command_data():
    return CommandData(
        command='ls',
        env={},
        cwd='/home/some-dir'
    )


@pytest.fixture
def fixt_credentials():
    return Credentials(
        username='test-user',
        password='test-pwd'
    )


@pytest.fixture
def fixt_worker_id():
    return '1.27.11.1:8181'


@pytest.fixture
def fixt_worker(fixt_worker_id):
    return Worker(
        worker_id=fixt_worker_id,
        worker_ref=sentinel.worker_ref,
    )