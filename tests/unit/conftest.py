from unittest.mock import Mock, sentinel

import pytest
from dq_broker.worker.notifier import WorkersNotifier
from dq_broker.worker.picker import FreeWorkersPicker

from dq_broker.infrastructure.repositories.worker import InMemoryWorkers
from dq_broker.infrastructure.websocket.clients import WorkerClient
from dq_broker.work.work_queue import WorkQueue
from dq_broker.worker.model import Worker


@pytest.fixture
def work_queue(fixt_work):
    work_queue = WorkQueue()
    work_queue.put(fixt_work)
    return work_queue


@pytest.fixture
def workers():
    repo = InMemoryWorkers()
    repo.put(
        Worker(
            worker_socket=sentinel.worker_socket_1,
            worker_ref=sentinel.worker_ref_1,
            host=sentinel.host_1,
        )
    )
    repo.put(
        Worker(
            worker_socket=sentinel.worker_socket_2,
            worker_ref=sentinel.worker_ref_2,
            host=sentinel.host_2,
        )
    )
    return repo


@pytest.fixture
def picker():
    return FreeWorkersPicker()


@pytest.fixture
def mock_worker_client():
    return Mock(spec=WorkerClient)


@pytest.fixture
def notifier(work_queue, workers, mock_worker_client, picker):
    return WorkersNotifier(
        work_queue=work_queue,
        workers=workers,
        worker_client=mock_worker_client,
        picker=picker
    )