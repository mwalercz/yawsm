import pytest

pytestmark = pytest.mark.asyncio


class TestWorkerConnectedAndHasWork:
    async def test(
            self, worker_connected_usecase, worker_has_work_usecase,
            work_saver, work_details_usecase,
            fixt_worker, fixt_work,
    ):
        work_id = await work_saver.save_new(fixt_work)
        fixt_work.set_id(work_id)
        await worker_connected_usecase.perform(fixt_worker)

        await worker_has_work_usecase.perform(fixt_worker.worker_id, fixt_work)

        work_details = await work_details_usecase.perform(
            work_id=fixt_work.work_id, username=fixt_work.credentials.username
        )

        last_event = work_details['events'][-1]
        assert last_event['status'] == 'processing'
        assert last_event['event_type'] == 'worker_has_work'








