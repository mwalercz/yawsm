import pytest

from dq_broker.work.model import NON_FINAL_STATUSES, WorkStatus

pytestmark = pytest.mark.asyncio


class TestAddWorksAndChangeStatus:
    async def test_create_two_works_and_change_status(
            self, fixt_new_work,
            fixt_user,
            new_work_usecase,
            list_work_usecase,
            change_work_status_usecase,
    ):
        work_id_1 = await new_work_usecase.perform(fixt_new_work, fixt_user)
        work_id_2 = await new_work_usecase.perform(fixt_new_work, fixt_user)

        await change_work_status_usecase.perform(
            from_statuses=NON_FINAL_STATUSES,
            to_status=WorkStatus.unknown.name,
            reason='broker_shutdown',
        )

        result = await list_work_usecase.perform(
            user_id=fixt_user.user_id
        )

        work_list = result['works']
        assert work_list[-2]['work_id'] == work_id_1
        assert work_list[-2]['status'] == 'unknown'
        assert work_list[-1]['work_id'] == work_id_2
        assert work_list[-1]['status'] == 'unknown'





