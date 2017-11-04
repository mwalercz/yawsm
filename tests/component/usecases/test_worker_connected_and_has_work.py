import pytest

pytestmark = pytest.mark.asyncio


class TestWorkerConnectedAndHasWork:
    async def test(
            self, worker_connected_usecase, worker_has_work_usecase,
            work_saver, work_details_usecase,
            fixt_new_worker_dto, fixt_work, fixt_user
    ):
        db_work = await work_saver.save(fixt_work, fixt_user.user_id)
        work = fixt_work._replace(work_id=db_work.work_id)
        await worker_connected_usecase.perform(fixt_new_worker_dto)

        await worker_has_work_usecase.perform(fixt_new_worker_dto.worker_socket, work)

        work_details = await work_details_usecase.perform(
            work_id=work.work_id, user_id=fixt_user.user_id
        )

        last_event = work_details['events'][-1]
        assert last_event['status'] == 'processing'
        assert last_event['reason'] == 'worker_has_work'








