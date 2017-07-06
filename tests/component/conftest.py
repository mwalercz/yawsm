from unittest.mock import Mock

import pytest
from dq_broker.dependencies.app import *
from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.db.work import Work, WorkEvent
from dq_broker.infrastructure.services.clients import ResponseClient, WorkerClient
from knot import Container


def register_mock_clients(c):
    c.add_service(Mock(spec=ResponseClient), 'response_client')
    c.add_service(Mock(spec=WorkerClient), 'worker_client')


def ssh(c):
    ssh = Mock(spec=SSHService)
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
    register_db_services(container)
    register_domain_services(container)
    register_infra_services(container)

    register_usecases(container)

    container.add_service(ssh)
    register_auth(container)

    register_controllers(container)

    return container


@pytest.yield_fixture
def clean_db(container):
    with container('objects').allow_sync():
        WorkEvent.delete().execute()
        Work.delete().execute()
    yield


@pytest.fixture
async def new_work_usecase(container):
    return container('usecases.user.new_work')


@pytest.fixture
async def kill_work_usecase(container):
    return container('usecases.user.kill_work')


@pytest.fixture
async def worker_connected_usecase(container):
    return container('usecases.worker.worker_connected')


@pytest.fixture
async def worker_requests_work_usecase(container):
    return container('usecases.worker.worker_requests_work')


@pytest.fixture
async def work_is_done_usecase(container):
    return container('usecases.worker.work_is_done')


@pytest.fixture
async def work_details_usecase(container):
    return container('usecases.user.work_details')


@pytest.fixture
async def list_work_usecase(container):
    return container('usecases.user.list_work')


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
def auth(container):
    return container('auth')


@pytest.fixture
def worker_headers(container):
    return {
        'x-api-key': container('conf')['worker']['api_key']
    }
