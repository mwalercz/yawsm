from unittest.mock import Mock, sentinel

import pytest

from dq_broker.domain.work.work_queue import WorkQueue
from dq_broker.domain.worker.model import Worker
from dq_broker.domain.worker.notifier import WorkersNotifier
from dq_broker.domain.worker.picker import FreeWorkersPicker
from dq_broker.infrastructure.repositories.worker import WorkerRepository
from dq_broker.infrastructure.websocket.clients import WorkerClient


@pytest.fixture
def work_queue(fixt_work):
    work_queue = WorkQueue()
    work_queue.put(fixt_work)
    return work_queue


@pytest.fixture
def workers_repo():
    repo = WorkerRepository()
    repo.put(
        Worker(
            worker_id=sentinel.worker_id_1,
            worker_ref=sentinel.worker_ref_1,
        )
    )
    repo.put(
        Worker(
            worker_id=sentinel.worker_id_2,
            worker_ref=sentinel.worker_ref_2
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
def notifier(work_queue, workers_repo, mock_worker_client, picker):
    return WorkersNotifier(
        work_queue=work_queue,
        workers_repo=workers_repo,
        worker_client=mock_worker_client,
        picker=picker
    )