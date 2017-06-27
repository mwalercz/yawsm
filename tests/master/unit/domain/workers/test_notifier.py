from tests.master.unit.domain.utils import assert_work_is_ready_sent_to_2_workers
from ws_dist_queue.master.domain.work.work_queue import WorkQueue
from ws_dist_queue.master.domain.workers.repository import WorkersRepository


class TestNotifier:
    def test_notify_when_work_queue_is_not_empty_and_two_workers_in_repo(
            self, notifier, mock_worker_client
    ):
        notifier.notify()

        assert_work_is_ready_sent_to_2_workers(mock_worker_client)

    def test_when_queue_is_empty_no_message_should_be_sent(
            self, notifier, mock_worker_client
    ):
        notifier.work_queue = WorkQueue()

        notifier.notify()

        mock_worker_client.send.assert_not_called()

    def test_when_there_are_no_workers_no_message_should_be_sent(
            self, notifier, mock_worker_client,
    ):
        notifier.workers_repo = WorkersRepository()

        notifier.notify()

        mock_worker_client.send.assert_not_called()
