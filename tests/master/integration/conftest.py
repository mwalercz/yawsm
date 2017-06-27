from unittest.mock import Mock

import pytest
from knot import Container

from definitions import MASTER_TESTING_CONFIG
from ws_dist_queue.master.dependencies.app import register_domain
from ws_dist_queue.master.infrastructure.clients import UserClient, WorkerClient
from ws_dist_queue.master.infrastructure.db.work import Work, WorkEvent


def register_mock_clients(c):
    c.add_service(Mock(spec=UserClient), 'user_client')
    c.add_service(Mock(spec=WorkerClient), 'worker_client')


@pytest.fixture
def container():
    container = Container(dict(
        config_path=MASTER_TESTING_CONFIG
    ))

    register_domain(container)
    register_mock_clients(container)

    return container


@pytest.yield_fixture
def clean_db(objects):
    with objects.allow_sync():
        Work.delete().execute()
        WorkEvent.delete().execute()
    yield
