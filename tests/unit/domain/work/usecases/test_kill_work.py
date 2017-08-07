from unittest.mock import Mock, sentinel

import asynctest
import pytest
from dq_broker.domain.exceptions import WorkNotFound, WorkerNotFound
from dq_broker.domain.work.model import WorkStatus
from dq_broker.domain.work.repository import WorkEventSaver, WorkFinder
from dq_broker.domain.work.usecases.kill import KillWorkUsecase
from dq_broker.domain.workers.repository import WorkersRepository
from dq_broker.infrastructure.db.work import Work

from dq_broker.domain.workers.model import Worker


@pytest.fixture
def mock_event_saver():
    return asynctest.Mock(spec=WorkEventSaver)


@pytest.fixture
def mock_work_finder():
    return asynctest.Mock(spec=WorkFinder)


@pytest.fixture
def mock_workers_repo():
    return Mock(spec=WorkersRepository)


@pytest.fixture
def kill_work_usecase(
        work_queue, mock_workers_repo, mock_worker_client,
        mock_event_saver, mock_work_finder
):
    return KillWorkUsecase(
        work_queue=work_queue,
        workers_repo=mock_workers_repo,
        worker_client=mock_worker_client,
        event_saver=mock_event_saver,
        work_finder=mock_work_finder,
    )


@pytest.mark.asyncio
class TestKillWorkUsecase:

    async def test_when_work_does_not_exist(
            self, kill_work_usecase, mock_work_finder
    ):
        """
        Given work not found in db,
        when kill work comes,
        then 'work_does_not_exist' should be returned.
        """
        mock_work_finder.find_by_work_id_and_username.side_effect = (
            WorkNotFound(work_id=5, username='does-not-exist')
        )

        result = await kill_work_usecase.perform(5, 'does-not-exist')

        assert result == {
            'status': 'work_does_not_exist'
        }
    async def test_when_work_in_final_status(
            self, kill_work_usecase, mock_work_finder
    ):
        """
        Given work in db in status finished_with_failure,
        when kill work comes,
        then 'work_already_in_final_status' should be returned.
        """
        mock_work_finder.find_by_work_id_and_username.return_value = (
            Work(
                work_id=5,
                status=WorkStatus.finished_with_failure.name
            )
        )

        result = await kill_work_usecase.perform(5, 'some-username')

        assert result == {
            'status': 'work_already_in_final_status',
            'work_status': 'finished_with_failure',
        }

    async def test_when_work_in_db_exist_and_work_is_in_queue(
            self, kill_work_usecase, fixt_work, work_queue,
            mock_work_finder
    ):
        """
        Given work in db in non-final status and work in queue,
        when kill work comes,
        then work is removed.
        """
        mock_work_finder.find_by_work_id_and_username.return_value = (
            Work(
                work_id=5,
                status=WorkStatus.processing.name,
                username='test-usr'
            )
        )
        fixt_work.work_id = 5
        work_queue.put(fixt_work)

        result = await kill_work_usecase.perform(
            work_id=5,
            username='test-usr',
        )

        assert result == {'status': 'work_killed_in_queue'}
        with pytest.raises(WorkNotFound):
            work_queue.pop_by_id(5)

    async def test_when_work_in_db_exist_and_work_is_in_workers(
            self, kill_work_usecase, fixt_work, mock_workers_repo,
            mock_work_finder, mock_worker_client
    ):
        """
        Given work in db in non-final status
        and work not in queue, and work in worker,
        when kill work comes,
        kill_work is sent to worker.
        """
        mock_work_finder.find_by_work_id_and_username.return_value = (
            Work(
                work_id=5,
                status=WorkStatus.processing.name,
                username='test-usr'
            )
        )
        fixt_work.work_id = 5
        mock_workers_repo.find_by_work_id.return_value = Worker(
            worker_id=sentinel.worker_id,
            worker_ref=sentinel.worker_ref,
            current_work=fixt_work
        )

        result = await kill_work_usecase.perform(
            work_id=5,
            username='test-user'
        )

        assert result == {
            'status': 'sig_kill_sent_to_worker',
            'worker_id': sentinel.worker_id,
        }
        mock_worker_client.send.assert_called_once_with(
            recipient=sentinel.worker_ref,
            action_name='kill_work'
        )

    async def test_when_work_in_db_exist_but_not_in_system(
            self, kill_work_usecase, fixt_work, mock_workers_repo,
            mock_work_finder, mock_worker_client
    ):
        """
        Given work in db in non-final status
        and work not in queue, and work not in worker,
        when kill work comes,
        exception is raised.
        """
        mock_work_finder.find_by_work_id_and_username.return_value = (
            Work(
                work_id=5,
                status=WorkStatus.processing.name,
                username='test-usr'
            )
        )
        fixt_work.work_id = 5
        mock_workers_repo.find_by_work_id.side_effect = WorkerNotFound

        with pytest.raises(WorkerNotFound):
            await kill_work_usecase.perform(
                work_id=5,
                username='test-user'
            )

        mock_worker_client.send.assert_not_called()

