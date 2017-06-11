from configparser import ConfigParser
from logging.config import dictConfig, fileConfig

import asyncio
import pytest
from peewee_async import Manager

from definitions import MASTER_TESTING_CONFIG
from ws_dist_queue.master.domain.work.model import Work, CommandData
from ws_dist_queue.master.infrastructure.auth.user import Credentials
from ws_dist_queue.master.infrastructure.db.work import database
from ws_dist_queue.master.infrastructure import db


@pytest.fixture
def fixt_conf():
    conf = ConfigParser()
    conf.read(MASTER_TESTING_CONFIG)
    # fileConfig(MASTER_TESTING_CONFIG)
    return conf


@pytest.fixture
def fixt_db(fixt_conf):
    conf = {
        'database': 'test_dist_queue',
        'user': 'test_dist_queue',
        'password': 'test_dist_queue',
        'host': 'localhost',
    }
    database.init(**conf)
    db.work.Work.create_table(True)
    db.work.WorkEvent.create_table(True)
    database.set_autocommit(False)
    return database


@pytest.yield_fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
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
