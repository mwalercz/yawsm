from unittest.mock import sentinel

import pytest

from yawsm.worker.actions.work_is_done.usecase import WorkIsDoneDto

pytestmark = pytest.mark.asyncio


class TestCreateAndFinishWork:
    async def test_create_and_finish_work(
            self, fixt_new_work, fixt_new_worker_dto, fixt_user,
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
        work_id = await new_work_usecase.perform(fixt_new_work, fixt_user)
        await worker_connected_usecase.perform(fixt_new_worker_dto)
        await worker_requests_work_usecase.perform(fixt_new_worker_dto.worker_socket)
        worker_client.send.assert_called_with(
            action_name='work_to_be_done',
            recipient=sentinel.worker_ref,
            body={
                'work_id': work_id,
                'cwd': fixt_new_work.cwd,
                'command': fixt_new_work.command,
                'env': fixt_new_work.env,
                'username': fixt_user.username,
                'password':fixt_user.password,
            }
        )
        await work_is_done_usecase.perform(
            dto=WorkIsDoneDto(
                worker_socket=fixt_new_worker_dto.worker_socket,
                work_id=work_id,
                status='finished_with_success',
                output='doc.txt something.sh'
            )
        )
        work_details = await work_details_usecase.perform(
            work_id, fixt_user.user_id
        )

        assert work_details['status'] == 'finished_with_success'
        work_events = work_details['events']
        assert len(work_events) == 3
        assert work_events[-1]['context']['output'] == 'doc.txt something.sh'
