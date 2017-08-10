import pytest

from dq_broker.domain.work.model import WorkStatus
from dq_broker.domain.worker.usecases.work_is_done import WorkIsDoneDto

pytestmark = pytest.mark.asyncio


class TestCreateAndKillWork:
    async def test_kill_work_twice(
            self, fixt_work, new_work_usecase, kill_work_usecase
    ):
        """
        Given new work was submitted, no worker in system and kill_work was submitted_once,
        When kill_work is performed second time,
        Then work_already_in_final_status should be returned.
        """
        work_id = await new_work_usecase.perform(fixt_work)
        kill_work_1_result = await kill_work_usecase.perform(
            work_id=work_id,
            username=fixt_work.credentials.username,
        )

        kill_work_2_result = await kill_work_usecase.perform(
            work_id=work_id,
            username=fixt_work.credentials.username
        )

        assert kill_work_1_result == {'status': 'work_killed_in_queue'}
        assert kill_work_2_result == {
            'status': 'work_already_in_final_status',
            'work_status': 'killed',
        }

    async def test_kill_work_after_giving_job_to_worker(
            self, fixt_work, fixt_worker, fixt_worker_id,
            new_work_usecase,
            kill_work_usecase,
            worker_connected_usecase,
            worker_requests_work_usecase,
            work_is_done_usecase,
            work_details_usecase,
    ):
        """
        Given new work was submitted, given to one worker,
        kill_work and work_is_done are performed,
        When work_details is performed,
        Then work_status should be killed.
        """
        work_id = await new_work_usecase.perform(fixt_work)
        await worker_connected_usecase.perform(fixt_worker)
        await worker_requests_work_usecase.perform(worker_id=fixt_worker_id)
        kill_work_result = await kill_work_usecase.perform(
            work_id=work_id, username=fixt_work.credentials.username
        )
        assert kill_work_result == {
            'status': 'sig_kill_sent_to_worker',
            'worker_id': fixt_worker.worker_id,
        }
        await work_is_done_usecase.perform(
            dto=WorkIsDoneDto(
                worker_id=fixt_worker.worker_id,
                work_id=work_id,
                status=WorkStatus.killed.name,
                output=None,
            )
        )

        work_details = await work_details_usecase.perform(
            work_id=work_id, username=fixt_work.credentials.username
        )

        assert work_details['status'] == 'killed'
        assert work_details['output'] is None

