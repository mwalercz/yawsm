import pytest

from dq_broker.domain.work.work_queue import WorkQueue
from dq_broker.infrastructure.repositories.worker import InMemoryWorkers
from tests.unit.domain.utils import assert_work_is_ready_sent_to_2_workers

pytestmark = pytest.mark.asyncio


class TestNotifier:
    async def test_notify_when_work_queue_is_not_empty_and_two_workers_in_repo(
            self, notifier, mock_worker_client
    ):
        await notifier.notify()

        assert_work_is_ready_sent_to_2_workers(mock_worker_client)

    async def test_when_queue_is_empty_no_message_should_be_sent(
            self, notifier, mock_worker_client
    ):
        notifier.work_queue = WorkQueue()

        await notifier.notify()

        mock_worker_client.send.assert_not_called()

    async def test_when_there_are_no_workers_no_message_should_be_sent(
            self, notifier, mock_worker_client,
    ):
        notifier.workers = InMemoryWorkers()

        await notifier.notify()

        mock_worker_client.send.assert_not_called()
