from unittest.mock import Mock

import asynctest
import pytest
from knot import Container

from dq_broker.dependencies.infrastructure.db import connect_to_db_and_create_tables
from dq_broker.dependencies.app import *
from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.db.work import Work, WorkEvent
from dq_broker.infrastructure.websocket.clients import ResponseClient, WorkerClient


def register_mock_clients(c):
    c.add_service(Mock(spec=ResponseClient), 'response_client')
    c.add_service(Mock(spec=WorkerClient), 'worker_client')


def ssh(c):
    ssh = asynctest.Mock(spec=SSHService)
    ssh.try_to_login.return_value = True
    return ssh


@pytest.fixture
def container(conf_path, event_loop):
    container = Container(dict(
        config_path=conf_path
    ))

    container.add_service(conf)
    container.add_service(lambda c: event_loop, 'loop')

    register_mock_clients(container)
    register_db(container)
    register_domain(container)
    register_ws_services(container)

    register_usecases(container)

    container.add_service(ssh)
    register_auth(container)

    register_ws(container)
    connect_to_db_and_create_tables()

    return container


@pytest.yield_fixture
def clean_db(container):
    with container('objects').allow_sync():
        WorkEvent.delete().execute()
        Work.delete().execute()
    yield


@pytest.fixture
async def new_work_usecase(container):
    return container('actions.work.new_work')


@pytest.fixture
async def kill_work_usecase(container):
    return container('actions.work.kill_work')


@pytest.fixture
async def worker_connected_usecase(container):
    return container('actions.worker.worker_connected')


@pytest.fixture
async def worker_requests_work_usecase(container):
    return container('actions.worker.worker_requests_work')


@pytest.fixture
async def worker_has_work_usecase(container):
    return container('actions.worker.worker_has_work')


@pytest.fixture
async def work_is_done_usecase(container):
    return container('actions.worker.work_is_done')


@pytest.fixture
async def worker_system_stat_usecase(container):
    return container('actions.worker.system_stat')


@pytest.fixture
async def worker_details_usecase(container):
    return container('actions.worker.details')


@pytest.fixture
async def worker_list_usecase(container):
    return container('actions.worker.list')


@pytest.fixture
async def work_details_usecase(container):
    return container('actions.work.work_details')


@pytest.fixture
async def list_work_usecase(container):
    return container('actions.work.list_work')


@pytest.fixture
async def change_work_status_usecase(container):
    return container('actions.work.change_status')


@pytest.fixture
async def new_user_usecase(container):
    return container('actions.user.new')


@pytest.fixture
async def worker_client(container):
    return container('worker_client')


@pytest.fixture
async def response_client(container):
    return container('response_client')


@pytest.fixture
async def work_finder(container):
    return container('work_finder')


@pytest.fixture
async def work_saver(container):
    return container('work_saver')


@pytest.fixture
def worker_auth(container):
    return container('worker_auth')


@pytest.fixture
def task_queue_consumer(container):
    return container('consumer')


@pytest.fixture
def worker_headers(container):
    return {'authorization': 'Basic dGVzdDpwYXNzd29yZA=='}
