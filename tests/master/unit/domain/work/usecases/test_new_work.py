import asynctest
from unittest.mock import sentinel

import pytest

from tests.master.unit.domain.utils import assert_work_is_ready_sent_to_2_workers
from ws_dist_queue.master.domain.work.repository import WorkSaver
from ws_dist_queue.master.domain.work.usecases.new_work import NewWorkUsecase
from ws_dist_queue.master.domain.work.work_queue import WorkQueue
from ws_dist_queue.master.domain.workers.repository import WorkersRepository


@pytest.mark.asyncio
class TestNewWorkUsecase:
    async def test_new_work_two_workers_no_work_in_queue(
            self, notifier, fixt_work, mock_worker_client
    ):
        """
        Given two workers in repo and no work in queue,
        When new work comes,
        Then two workers should be notified.
        """
        work_saver = asynctest.Mock(spec=WorkSaver)
        work_queue = WorkQueue()
        work_saver.save_new.return_value = sentinel.work_id
        usecase = NewWorkUsecase(
            work_queue=work_queue,
            work_saver=work_saver,
            workers_notifier=notifier
        )

        await usecase.perform(fixt_work)

        assert fixt_work.work_id == sentinel.work_id
        assert_work_is_ready_sent_to_2_workers(mock_worker_client)

    async def test_new_work_zero_workers_no_work_in_queue(
            self, notifier, fixt_work, mock_worker_client
    ):
        """
        Given no workers in repo and no work in queue,
        When new work comes,
        Then nobody should be notified.
        """
        work_saver = asynctest.Mock(spec=WorkSaver)
        work_queue = WorkQueue()
        notifier.workers_repo = WorkersRepository()
        work_saver.save_new.return_value = sentinel.work_id
        usecase = NewWorkUsecase(
            work_queue=work_queue,
            work_saver=work_saver,
            workers_notifier=notifier
        )

        await usecase.perform(fixt_work)

        assert fixt_work.work_id == sentinel.work_id
        mock_worker_client.send.assert_not_called()

