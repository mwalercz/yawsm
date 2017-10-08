import asynctest
import pytest

from dq_broker.work.work_queue import WorkQueue
from dq_broker.infrastructure.repositories.work import WorkSaver
from dq_broker.infrastructure.repositories.worker import InMemoryWorkers
from dq_broker.work.actions.new.usecase import NewWorkUsecase
from tests.unit.domain.utils import assert_work_is_ready_sent_to_2_workers


@pytest.mark.asyncio
class TestNewWorkUsecase:
    async def test_new_work_two_workers_no_work_in_queue(
            self, notifier, fixt_db_work, fixt_new_work, fixt_user, mock_worker_client
    ):
        """
        Given two worker in repo and no work in queue,
        When new work comes,
        Then two worker should be notified.
        """
        work_saver = asynctest.Mock(spec=WorkSaver)
        work_queue = WorkQueue()
        work_saver.save.return_value = fixt_db_work
        usecase = NewWorkUsecase(
            work_queue=work_queue,
            work_saver=work_saver,
            workers_notifier=notifier
        )

        await usecase.perform(fixt_new_work, fixt_user)

        assert_work_is_ready_sent_to_2_workers(mock_worker_client)

    async def test_new_work_zero_workers_no_work_in_queue(
            self, notifier, fixt_db_work, fixt_new_work, fixt_user, mock_worker_client
    ):
        """
        Given no worker in repo and no work in queue,
        When new work comes,
        Then nobody should be notified.
        """
        work_saver = asynctest.Mock(spec=WorkSaver)
        work_queue = WorkQueue()
        notifier.workers = InMemoryWorkers()
        work_saver.save.return_value = fixt_db_work
        usecase = NewWorkUsecase(
            work_queue=work_queue,
            work_saver=work_saver,
            workers_notifier=notifier
        )

        await usecase.perform(fixt_new_work, fixt_user)

        mock_worker_client.send.assert_not_called()
