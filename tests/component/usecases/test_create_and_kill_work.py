from unittest.mock import ANY, call

import pytest

from yawsm.work.model import WorkStatus, KillWork
from yawsm.worker.actions.work_is_done.usecase import WorkIsDoneDto

pytestmark = pytest.mark.asyncio


class TestCreateAndKillWork:
    async def test_kill_work_twice(
            self,
            fixt_new_work,
            new_work_usecase,
            kill_work_usecase,
            fixt_user,
            task_queue_consumer,
            worker_client,
    ):
        """
        Given READY work was submitted, no worker in system and kill_work was submitted_once,
        When kill_work is performed second time,
        Then another kill_work should be accepted.
        """

        work_id = await new_work_usecase.perform(fixt_new_work, fixt_user)
        await task_queue_consumer.consume_one()
        kill_work_1_result = await kill_work_usecase.perform(
            KillWork(
                work_id=work_id,
                user_id=fixt_user.user_id
            )
        )
        kill_work_2_result = await kill_work_usecase.perform(
            KillWork(
                work_id=work_id,
                user_id=fixt_user.user_id
            )
        )

        assert kill_work_1_result == {
            'status': 'ok',
            'info': 'work_cancelled_in_queue',
        }
        assert kill_work_2_result == {
            'status': 'error',
            'reason': 'work_already_in_final_status',
            'work_status': 'CANCELLED'
        }

        assert worker_client.send.mock_calls == []

    async def test_kill_work_after_giving_job_to_worker(
            self,
            fixt_new_work,
            fixt_user,
            fixt_new_worker_dto,
            fixt_new_worker_dto_socket,
            worker_client,
            new_work_usecase,
            kill_work_usecase,
            worker_connected_usecase,
            worker_requests_work_usecase,
            work_is_done_usecase,
            work_details_usecase,
            task_queue_consumer,
    ):
        """
        Given READY work was submitted, given to one worker,
        kill_work and work_is_done are performed,
        When work_details is performed,
        Then work_status should be CANCELLED.
        """
        worker_ref = fixt_new_worker_dto.worker_ref

        work_id = await new_work_usecase.perform(fixt_new_work, fixt_user)
        await task_queue_consumer.consume_one()
        await worker_connected_usecase.perform(fixt_new_worker_dto)
        await worker_requests_work_usecase.perform(worker_socket=fixt_new_worker_dto_socket)
        kill_work_result = await kill_work_usecase.perform(
            KillWork(work_id=work_id, user_id=fixt_user.user_id)
        )
        assert kill_work_result == {
            'status': 'ok',
            'info': 'cancel_work_sent_to_worker',
            'worker_socket': '1.27.11.1:8181',
        }
        await work_is_done_usecase.perform(
            dto=WorkIsDoneDto(
                worker_socket=fixt_new_worker_dto.worker_socket,
                work_id=work_id,
                status='KILLED',
                output=None,
            )
        )

        assert worker_client.send.mock_calls == [
            call(action_name='work_is_ready', recipient=worker_ref),
            call(action_name='work_to_be_done', body=ANY, recipient=worker_ref),
            call(action_name='cancel_work', recipient=worker_ref),
            call(action_name='work_is_done_ack', recipient=worker_ref),
        ]

        work_details = await work_details_usecase.perform(
            work_id=work_id, user_id=fixt_user.user_id
        )

        assert work_details['status'] == 'CANCELLED'
        assert work_details['output'] is None
