import asynctest
import pytest

from yawsm.exceptions import WorkNotFound
from yawsm.infrastructure.db.work import WorkEvent, Work
from yawsm.infrastructure.repositories.work import WorkFinder
from yawsm.work.actions.details.usecase import WorkDetailsUsecase
from yawsm.work.model import WorkStatus
from tests.unit.utils import parse_to_datetime


@pytest.fixture
def fixt_db_work_id():
    return 111


@pytest.fixture
def fixt_db_events(fixt_db_work_id, fixt_new_worker_dto_socket):
    return [
        WorkEvent(
            work_id=fixt_db_work_id,
            event_id=1,
            event_type='work_created',
            status=WorkStatus.READY.name,
            created_at=parse_to_datetime('2017-01-02T20:21:23'),
        ),
        WorkEvent(
            work_id=fixt_db_work_id,
            event_id=2,
            event_type='work_assigned',
            status=WorkStatus.PROCESSING.name,
            created_at=parse_to_datetime('2017-01-02T20:21:24'),
            context={
                'worker_socket': fixt_new_worker_dto_socket
            },
        ),
        WorkEvent(
            work_id=fixt_db_work_id,
            event_id=3,
            event_type='work_finished',
            status=WorkStatus.FINISHED.name,
            created_at=parse_to_datetime('2017-01-02T20:21:25'),
            context={
                'worker_socket': fixt_new_worker_dto_socket,
                'output': 'this.txt that.sh',
            }
        )
    ]


@pytest.fixture
def fixt_db_work(fixt_db_work_id, fixt_db_events):
    return Work(
        work_id=fixt_db_work_id,
        command='ls',
        cwd='/home/user',
        env={},
        exit_code=0,
        username='test-user',
        output='this.txt that.sh',
        status=WorkStatus.FINISHED.name,
        created_at=parse_to_datetime('2017-01-02T20:21:23'),
        events=fixt_db_events
    )


@pytest.mark.asyncio
class TestWorkDetails:
    async def test_work_details_when_work_exists(
            self, fixt_db_work, fixt_db_work_id, fixt_new_worker_dto_socket, fixt_user
    ):
        """
        Given work with three events found in repository,
        When work_details is performed,
        Then work should be returned.
        """
        mock_work_finder = asynctest.Mock(spec=WorkFinder)
        mock_work_finder \
            .find_by_work_id_and_user_id_with_events \
            .return_value = fixt_db_work
        work_details_usecase = WorkDetailsUsecase(work_finder=mock_work_finder)

        result = await work_details_usecase.perform(fixt_db_work_id, fixt_user.user_id)

        mock_work_finder \
            .find_by_work_id_and_user_id_with_events \
            .assert_called_once_with(fixt_db_work_id, fixt_user.user_id)
        assert result == {
            'work_id': fixt_db_work_id,
            'command': 'ls',
            'cwd': '/home/user',
            'environment': {},
            'exit_code': 0,
            'output': 'this.txt that.sh',
            'status': 'FINISHED',
            'created_at': '2017-01-02T20:21:23',
            'events': [
                {
                    'event_id': 1,
                    'reason': 'work_created',
                    'status': 'READY',
                    'created_at': '2017-01-02T20:21:23',
                    'context': {},
                },
                {
                    'event_id': 2,
                    'reason': 'work_assigned',
                    'status': 'PROCESSING',
                    'created_at': '2017-01-02T20:21:24',
                    'context': {
                        'worker_socket': fixt_new_worker_dto_socket
                    }
                },
                {
                    'event_id': 3,
                    'reason': 'work_finished',
                    'status': 'FINISHED',
                    'created_at': '2017-01-02T20:21:25',
                    'context': {
                        'worker_socket': fixt_new_worker_dto_socket,
                        'output': 'this.txt that.sh',
                    }
                }
            ]

        }

    async def test_work_details_when_work_not_found(self, fixt_db_work_id, fixt_user):
        """
        Given work not found in repository,
        When work_details is performed,
        Then exception should be raised.
        """
        mock_work_finder = asynctest.Mock(spec=WorkFinder)
        mock_work_finder \
            .find_by_work_id_and_user_id_with_events \
            .side_effect = WorkNotFound(work_id=fixt_db_work_id, user_id=fixt_user.user_id)
        work_details_usecase = WorkDetailsUsecase(work_finder=mock_work_finder)

        with pytest.raises(WorkNotFound) as exc:
            await work_details_usecase.perform(
                work_id=fixt_db_work_id,
                user_id=fixt_user.user_id
            )

        assert exc.value.work_id == fixt_db_work_id
        assert exc.value.username == fixt_user.user_id
        mock_work_finder \
            .find_by_work_id_and_user_id_with_events \
            .assert_called_once_with(fixt_db_work_id, fixt_user.user_id)
