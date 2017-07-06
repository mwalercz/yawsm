from unittest.mock import sentinel

import pytest

from dq_broker.domain.workers.usecases.work_is_done import WorkIsDoneDto

pytestmark = pytest.mark.asyncio


class TestCreateAndFinishWork:
    async def test_create_and_finish_work(
            self,  fixt_work, fixt_worker,
            new_work_usecase,
            worker_connected_usecase,
            worker_requests_work_usecase,
            work_is_done_usecase,
            work_details_usecase,
            worker_client,
    ):
        """
        Given new work was submitted, given to one worker
        and work_is_done is performed,
        When work_details is performed,
        Then work_status should be finished_with success
        and last event should have output.
        """
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
        work_events = work_details['events']
        assert len(work_events) == 3
        assert work_events[-1]['context']['output'] == 'doc.txt something.sh'





