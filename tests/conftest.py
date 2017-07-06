import asyncio
from configparser import ConfigParser
from unittest.mock import sentinel

import os
import pytest

import dq_broker
from dq_broker.domain.work.model import Work, CommandData
from dq_broker.infrastructure.auth.user import Credentials
from dq_broker.infrastructure.db.work import database
from peewee_async import Manager

from definitions import ROOT_DIR
from dq_broker.domain.workers.model import Worker


def pytest_addoption(parser):
    parser.addoption(
        "--settings", action="store",
        default="develop.ini", help="config name"
    )


@pytest.fixture
def user_headers():
    return {
        'username': 'some-user',
        'password': 'some-pass',
        'x-parent-pid': 'parent-pid',
    }


@pytest.fixture
def cookie_headers():
    return {
        'x-cookie': 'some-cookie-1',
        'x-parent-pid': 'parent-pid',
    }


@pytest.fixture
def conf_path(request):
    conf_name = request.config.getoption("--settings")
    conf_path = os.path.join(ROOT_DIR, 'dq_broker/conf/', conf_name)
    return conf_path


@pytest.fixture
def fixt_conf(conf_path):
    conf = ConfigParser()
    conf.read(conf_path)
    return conf


@pytest.fixture
def fixt_db(fixt_conf):
    database.init(**fixt_conf['db'])
    dq_broker.infrastructure.db.work.Work.create_table(True)
    dq_broker.infrastructure.db.work.WorkEvent.create_table(True)
    database.set_autocommit(False)
    return database


@pytest.fixture
def event_loop(request):
    return asyncio.get_event_loop()


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
def fixt_username():
    return 'test-user'


@pytest.fixture
def fixt_credentials(fixt_username):
    return Credentials(
        username=fixt_username,
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
