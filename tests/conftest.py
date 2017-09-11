import asyncio
from configparser import ConfigParser
from unittest.mock import sentinel

import os
import pytest
import random

import dq_broker
from dq_broker.domain.user.model import User
from dq_broker.domain.work.model import Work, Credentials
from dq_broker.infrastructure.db.user import User as DbUser
from dq_broker.infrastructure.db.base import database
from peewee_async import Manager

from definitions import ROOT_DIR
from dq_broker.domain.worker.model import Worker
from dq_broker.infrastructure.http.controllers.schema import NewWorkDto
from dq_broker.infrastructure.websocket.controllers.worker.worker_system_stat import WorkerSystemStat


def pytest_addoption(parser):
    parser.addoption(
        "--settings", action="store",
        default="develop.ini", help="config name"
    )


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
def fixt_objects(fixt_db, event_loop) -> Manager:
    objects = Manager(database=fixt_db, loop=event_loop)
    return objects


@pytest.fixture
def fixt_work(fixt_new_work, fixt_credentials):
    work_id = random.randint(0, 9999999)
    return Work(
        work_id=work_id,
        command=fixt_new_work.command,
        env=fixt_new_work.env,
        cwd=fixt_new_work.cwd,
        credentials=fixt_credentials
    )


@pytest.fixture
def fixt_db_work(fixt_work):
    return dq_broker.infrastructure.db.work.Work(
        work_id=fixt_work.work_id,
        command=fixt_work.command,
        cwd=fixt_work.cwd,
        env=fixt_work.env,
        user_id=1
    )


@pytest.fixture
def fixt_new_work():
    instance = NewWorkDto({
        'command': 'ls',
        'env': {},
        'cwd': 'home/some-dir'
    })
    instance.validate()
    return instance


@pytest.fixture
def fixt_user(fixt_saved_user, fixt_credentials):
    return User(
        user_id=fixt_saved_user.user_id,
        username=fixt_saved_user.username,
        password=fixt_credentials.password,
        is_admin=fixt_saved_user.is_admin,
    )


@pytest.fixture
def fixt_saved_user(fixt_username, fixt_objects: Manager):
    with fixt_objects.allow_sync():
        user, was_created = DbUser.get_or_create(
            username=fixt_username,
            defaults={'username': fixt_username, 'is_admin': False}
        )
    return user


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
def fixt_username():
    return 'test-user'


@pytest.fixture
def fixt_credentials(fixt_username):
    return Credentials(
        username=fixt_username,
        password='test-pwd'
    )


@pytest.fixture
def fixt_worker_socket():
    return '1.27.11.1:8181'


@pytest.fixture
def fixt_worker(fixt_worker_socket):
    return Worker(
        worker_socket=fixt_worker_socket,
        worker_ref=sentinel.worker_ref,
    )


@pytest.fixture
def worker_system_stat():
    stat = WorkerSystemStat(
        {
            'cpu': {
                'count': 3,
                'load_1': 1.1,
                'load_5': 2.4,
                'load_15': 1.9,
            },
            'memory': {
                'total': 123,
                'available': 20
            }
        }
    )
    stat.validate()
    return stat
