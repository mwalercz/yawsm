import pytest

pytestmark = pytest.mark.asyncio


class TestCreateAndListWork:
    async def test_create_two_works_and_list_them(
            self, fixt_work,
            new_work_usecase,
            list_work_usecase,
    ):
        work_id_1 = await new_work_usecase.perform(fixt_work)
        work_id_2 = await new_work_usecase.perform(fixt_work)

        result = await list_work_usecase.perform(
            username=fixt_work.credentials.username
        )

        work_list = result['works']
        assert len(work_list) >= 2
        assert work_list[-2]['work_id'] == work_id_1
        assert work_list[-2]['status'] == 'new'
        assert work_list[-1]['work_id'] == work_id_2
        assert work_list[-1]['status'] == 'new'




