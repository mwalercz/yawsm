import asynctest
import pytest

from dq_broker.domain.exceptions import WorkNotFound
from dq_broker.domain.work.model import WorkStatus
from dq_broker.domain.work.usecases.details import WorkDetailsUsecase
from dq_broker.infrastructure.db.work import WorkEvent, Work
from dq_broker.infrastructure.repositories.work import WorkFinder
from tests.unit.domain.utils import parse_to_datetime


@pytest.fixture
def fixt_db_work_id():
    return 111


@pytest.fixture
def fixt_db_events(fixt_db_work_id, fixt_worker_id):
    return [
        WorkEvent(
            work_id=fixt_db_work_id,
            event_id=1,
            event_type='work_created',
            status=WorkStatus.new.name,
            created_at=parse_to_datetime('2017-01-02T20:21:23'),
        ),
        WorkEvent(
            work_id=fixt_db_work_id,
            event_id=2,
            event_type='work_assigned',
            status=WorkStatus.processing.name,
            created_at=parse_to_datetime('2017-01-02T20:21:24'),
            context={
                'worker_id': fixt_worker_id
            },
        ),
        WorkEvent(
            work_id=fixt_db_work_id,
            event_id=3,
            event_type='work_finished',
            status=WorkStatus.finished_with_success.name,
            created_at=parse_to_datetime('2017-01-02T20:21:25'),
            context={
                'worker_id': fixt_worker_id,
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
        username='test-user',
        output='this.txt that.sh',
        status=WorkStatus.finished_with_success.name,
        created_at=parse_to_datetime('2017-01-02T20:21:23'),
        events=fixt_db_events
    )


@pytest.mark.asyncio
class TestWorkDetails:
    async def test_work_details_when_work_exists(
            self, fixt_db_work, fixt_db_work_id, fixt_worker_id
    ):
        """
        Given work with three events found in repository,
        When work_details is performed,
        Then work should be returned.
        """
        mock_work_finder = asynctest.Mock(spec=WorkFinder)
        mock_work_finder \
            .find_by_work_id_and_username_with_events \
            .return_value = fixt_db_work
        work_details_usecase = WorkDetailsUsecase(work_finder=mock_work_finder)

        result = await work_details_usecase.perform(fixt_db_work_id, 'test-user')

        mock_work_finder \
            .find_by_work_id_and_username_with_events \
            .assert_called_once_with(fixt_db_work_id, 'test-user')
        assert result == {
            'work_id': fixt_db_work_id,
            'command': 'ls',
            'cwd': '/home/user',
            'environment': {},
            'output': 'this.txt that.sh',
            'status': 'finished_with_success',
            'created_at': '2017-01-02T20:21:23',
            'events': [
                {
                    'event_id': 1,
                    'event_type': 'work_created',
                    'status': 'new',
                    'created_at': '2017-01-02T20:21:23',
                    'context': {},
                },
                {
                    'event_id': 2,
                    'event_type': 'work_assigned',
                    'status': 'processing',
                    'created_at': '2017-01-02T20:21:24',
                    'context': {
                        'worker_id': fixt_worker_id
                    }
                },
                {
                    'event_id': 3,
                    'event_type': 'work_finished',
                    'status': 'finished_with_success',
                    'created_at': '2017-01-02T20:21:25',
                    'context': {
                        'worker_id': fixt_worker_id,
                        'output': 'this.txt that.sh',
                    }
                }
            ]

        }

    async def test_work_details_when_work_not_found(self, fixt_db_work_id):
        """
        Given work not found in repository,
        When work_details is performed,
        Then exception should be raised.
        """
        mock_work_finder = asynctest.Mock(spec=WorkFinder)
        mock_work_finder \
            .find_by_work_id_and_username_with_events \
            .side_effect = WorkNotFound(work_id=fixt_db_work_id, username='test-user')
        work_details_usecase = WorkDetailsUsecase(work_finder=mock_work_finder)

        with pytest.raises(WorkNotFound) as exc:
            await work_details_usecase.perform(
                work_id=fixt_db_work_id,
                username='test-user'
            )

        assert exc.value.work_id == fixt_db_work_id
        assert exc.value.username == 'test-user'
        mock_work_finder \
            .find_by_work_id_and_username_with_events \
            .assert_called_once_with(fixt_db_work_id, 'test-user')
