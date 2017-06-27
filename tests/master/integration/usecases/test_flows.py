from unittest.mock import sentinel

import pytest

from ws_dist_queue.master.domain.workers.usecases.work_is_done import WorkIsDoneDto

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def new_work_usecase(container):
    return container('usecases.user.new_work')


@pytest.fixture
async def kill_work_usecase(container):
    return container('usecases.user.kill_work')


@pytest.fixture
async def worker_connected_usecase(container):
    return container('usecases.worker.worker_connected')


@pytest.fixture
async def worker_requests_work_usecase(container):
    return container('usecases.worker.worker_requests_work')


@pytest.fixture
async def work_is_done_usecase(container):
    return container('usecases.worker.work_is_done')


@pytest.fixture
async def work_details_usecase(container):
    return container('usecases.user.work_details')


@pytest.fixture
async def worker_client(container):
    return container('worker_client')


@pytest.fixture
async def work_finder(container):
    return container('work_finder')


class TestFlow:

    async def test_new_work_kill_work_kill_work(
            self, fixt_work, new_work_usecase, kill_work_usecase
    ):
        work_id = await new_work_usecase.perform(fixt_work)
        assert await kill_work_usecase.perform(
            work_id=work_id,
            username=fixt_work.credentials.username,
        ) == {'status': 'work_killed_in_queue'}

        assert await kill_work_usecase.perform(
            work_id=work_id,
            username=fixt_work.credentials.username,
        ) == {
            'status': 'work_already_in_final_status',
            'work_status': 'killed',
        }

    async def test_new_work_worker_connected_worker_requests_work(
            self,  fixt_work, fixt_worker,
            new_work_usecase,
            worker_connected_usecase,
            worker_requests_work_usecase,
            work_is_done_usecase,
            work_details_usecase,
            worker_client,
    ):

        work_id = await new_work_usecase.perform(fixt_work)
        worker_connected_usecase.perform(fixt_worker)
        await worker_requests_work_usecase.perform(fixt_worker.worker_id)

        worker_client.send.assert_called_with(
            action_name='work_to_be_done',
            recipient=sentinel.worker_ref,
            body=fixt_work,
        )

        await work_is_done_usecase.perform(
            dto=WorkIsDoneDto(
                worker_id=fixt_worker.worker_id,
                work_id=work_id,
                status='finished_with_success',
                output='doc.txt something.sh'
            )
        )
        result = await work_details_usecase.perform(
            work_id, fixt_work.credentials.username
        )

        work_details = result['work']
        assert work_details['status'] == 'finished_with_success'
        assert work_details['events'][-1]['context']['output'] == 'doc.txt something.sh'





