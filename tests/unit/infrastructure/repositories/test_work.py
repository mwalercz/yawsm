import logging

import pytest

from yawsm.exceptions import WorkNotFound
from yawsm.infrastructure.db.work import WorkEvent
from yawsm.infrastructure.repositories.work import WorkSaver, WorkFinder, WorkEventSaver
from yawsm.work.model import WorkStatus

log = logging.getLogger(__name__)


@pytest.fixture
def fixt_work_saver(fixt_objects):
    return WorkSaver(objects=fixt_objects)


@pytest.fixture
def fixt_event_saver(fixt_objects):
    return WorkEventSaver(objects=fixt_objects)


@pytest.fixture
def fixt_finder(fixt_objects):
    return WorkFinder(objects=fixt_objects)


@pytest.mark.asyncio
class TestWorkSaverAndFinder:
    async def test_save_work_and_retrieve_work_with_events(
            self, fixt_work_saver, fixt_work, fixt_finder, fixt_saved_user
    ):
        db_work = await fixt_work_saver.save(fixt_work, fixt_saved_user.user_id)
        work_found = await fixt_finder.find_by_work_id_and_user_id_with_events(
            db_work.work_id, fixt_saved_user.user_id
        )

        assert work_found.work_id == db_work.work_id
        assert work_found.status == 'new'
        event = work_found.events[0]
        assert event.status == 'new'
        assert event.event_type == 'work_created'

    async def test_add_events_and_retrive_work_with_added_events(
            self, fixt_work_saver, fixt_event_saver, fixt_finder,
            fixt_work, fixt_saved_user
    ):
        work_id = await fixt_work_saver.save(
            fixt_work, fixt_saved_user.user_id
        )

        event_1 = WorkEvent(
            work_id=work_id,
            reason='worker_started_processing',
            context={'worker_socket': '1'},
            work_status=WorkStatus.processing.name,
        )
        event_2 = WorkEvent(
            work_id=work_id,
            reason='worker_finished_processing',
            work_status=WorkStatus.finished_with_failure.name,
            context={'worker_socket': '2'}
        )

        await fixt_event_saver.save_event(event_1)
        await fixt_event_saver.save_event(event_2)

        work_found = await fixt_finder.find_by_work_id_and_user_id_with_events(
            work_id, fixt_saved_user.user_id
        )

        assert work_found.status == 'finished_with_failure'
        assert len(work_found.events) == 3
        assert work_found.events[0].status == 'new'
        assert work_found.events[1].status == 'processing'
        assert work_found.events[1].context == {'worker_socket': '1'}
        assert work_found.events[2].status == 'finished_with_failure'
        assert work_found.events[2].context == {'worker_socket': '2'}

    async def test_when_no_results_find_by_work_id_should_raise_error(
            self, fixt_finder
    ):
        with pytest.raises(WorkNotFound):
            await fixt_finder.find_by_work_id_and_user_id_with_events(
                work_id=9999999,
                user_id=4231412341
            )

    async def test_when_no_results_find_by_work_id_and_username_should_raise(
            self, fixt_finder
    ):
        with pytest.raises(WorkNotFound) as exc:
            await fixt_finder.find_by_work_id_and_user_id(
                work_id=9999999, user_id=12323213213
            )

        assert exc.value.work_id == 9999999
        assert exc.value.username == 12323213213

    async def test_when_no_results_find_by_username_should_return_empty_list(
            self, fixt_finder
    ):
        assert [] == await fixt_finder.find_by_user_id(user_id=132213212312)

    async def test_find_by_work_id_and_username(
            self, fixt_work_saver, fixt_work, fixt_finder, fixt_saved_user
    ):
        db_work = await fixt_work_saver.save(fixt_work, fixt_saved_user.user_id)

        work_found = await fixt_finder.find_by_work_id_and_user_id(
            user_id=fixt_saved_user.user_id,
            work_id=db_work.work_id,
        )

        assert work_found.work_id == db_work.work_id
        assert work_found.status == 'new'
        assert work_found.user_id == fixt_saved_user.user_id

    async def test_find_by_user_id(
            self, fixt_work_saver, fixt_work, fixt_finder, fixt_saved_user
    ):
        db_work = await fixt_work_saver.save(fixt_work, fixt_saved_user.user_id)

        work_list = await fixt_finder.find_by_user_id(
            user_id=fixt_saved_user.user_id
        )

        assert [
            work for work in work_list
            if work.work_id == db_work.work_id
        ][0].user_id == fixt_saved_user.user_id



