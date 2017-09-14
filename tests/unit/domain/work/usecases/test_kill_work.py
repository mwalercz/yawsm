from unittest.mock import Mock, sentinel

import asynctest
import pytest

from dq_broker.domain.exceptions import WorkNotFound, WorkerNotFound
from dq_broker.domain.work.model import WorkStatus, Credentials
from dq_broker.domain.work.usecases.kill import KillWorkUsecase
from dq_broker.domain.worker.model import Worker
from dq_broker.infrastructure.db.work import Work
from dq_broker.infrastructure.repositories.work import WorkEventSaver, WorkFinder
from dq_broker.infrastructure.repositories.worker import InMemoryWorkers


@pytest.fixture
def mock_event_saver():
    return asynctest.Mock(spec=WorkEventSaver)


@pytest.fixture
def mock_work_finder():
    return asynctest.Mock(spec=WorkFinder)


@pytest.fixture
def mock_workers():
    return Mock(spec=InMemoryWorkers)


@pytest.fixture
def kill_work_usecase(
        work_queue, mock_workers, mock_worker_client,
        mock_event_saver, mock_work_finder
):
    return KillWorkUsecase(
        work_queue=work_queue,
        workers=mock_workers,
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
        mock_work_finder.find_by_work_id_and_user_id.side_effect = (
            WorkNotFound(work_id=5, user_id='does-not-exist')
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
        mock_work_finder.find_by_work_id_and_user_id.return_value = (
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
        mock_work_finder.find_by_work_id_and_user_id.return_value = (
            Work(
                work_id=fixt_work.work_id,
                status=WorkStatus.processing.name,
                username='test-usr'
            )
        )
        work_queue.put(fixt_work)

        result = await kill_work_usecase.perform(
            work_id=fixt_work.work_id,
            user_id='test-usr',
        )

        assert result == {'status': 'work_killed_in_queue'}
        with pytest.raises(WorkNotFound):
            work_queue.pop_by_id(5)

    async def test_when_work_in_db_exist_and_work_is_in_workers(
            self, kill_work_usecase, fixt_credentials, mock_workers,
            mock_work_finder, mock_worker_client
    ):
        """
        Given work in db in non-final status
        and work not in queue, and work in worker,
        when kill work comes,
        kill_work is sent to worker.
        """
        work = self._get_work_not_in_queue()
        mock_work_finder.find_by_work_id_and_user_id.return_value = (
            Work(
                work_id=work.work_id,
                status=WorkStatus.processing.name,
                username='test-usr'
            )
        )
        mock_workers.find_by_work_id.return_value = Worker(
            worker_socket=sentinel.worker_socket,
            worker_ref=sentinel.worker_ref,
            current_work=work.work_id,
            host_id=1,
            worker_id=1,
        )

        result = await kill_work_usecase.perform(
            work_id=work.work_id,
            user_id='test-user'
        )

        assert result == {
            'status': 'sig_kill_sent_to_worker',
            'worker_socket': sentinel.worker_socket,
        }
        mock_worker_client.send.assert_called_once_with(
            recipient=sentinel.worker_ref,
            action_name='kill_work'
        )

    def _get_work_not_in_queue(self):
        return Work(
            work_id=5,
            cwd='lala',
            command='blabla',
            env={},
            credentials=Credentials(
                username='test-usr',
                password='test-pwd'
            ),
        )

    async def test_when_work_in_db_exist_but_not_in_system(
            self, kill_work_usecase, mock_workers,
            mock_work_finder, mock_worker_client
    ):
        """
        Given work in db in non-final status
        and work not in queue, and work not in worker,
        when kill work comes,
        exception is raised.
        """
        work = self._get_work_not_in_queue()
        mock_work_finder.find_by_work_id_and_user_id.return_value = (
            Work(
                work_id=work.work_id,
                status=WorkStatus.processing.name,
                username='test-usr'
            )
        )
        mock_workers.find_by_work_id.side_effect = WorkerNotFound

        with pytest.raises(WorkerNotFound):
            await kill_work_usecase.perform(
                work_id=work.work_id,
                user_id='test-user'
            )

        mock_worker_client.send.assert_not_called()

