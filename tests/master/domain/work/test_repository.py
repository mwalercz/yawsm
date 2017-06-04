import pytest

from ws_dist_queue.master.domain.work.repository import WorkSaver


@pytest.mark.asyncio
class TestWorkSaverAndFinder:
    @pytest.fixture
    def fixt_saver(self, fixt_objects):
        return WorkSaver(objects=fixt_objects)

    async def test_save(self, fixt_saver, fixt_work, fixt_objects):
        async with fixt_saver.objects.transaction() as txn:
            await fixt_saver.save_new(fixt_work)
            txn.rollback(begin=False)
        print(fixt_work)