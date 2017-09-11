import pytest

from dq_broker.domain.worker.model import Worker
from dq_broker.domain.worker.usecases.details import WorkerDetailsUsecase
from dq_broker.domain.worker.usecases.list import WorkerListUsecase
from dq_broker.domain.worker.usecases.worker_connected import WorkerConnectedUsecase
from dq_broker.domain.worker.usecases.worker_system_stat import WorkerSystemStatUsecase

from dq_broker.infrastructure.websocket.controllers.worker.worker_system_stat import WorkerSystemStat

pytestmark = pytest.mark.asyncio


class TestConnectedWorkerShouldBeReturnedInDetailsAndList:
    async def test_given_worker_connected_system_stat_when_worker_details_then_it_should_exist(
            self,
            worker_connected_usecase: WorkerConnectedUsecase,
            worker_system_stat_usecase: WorkerSystemStatUsecase,
            worker_details_usecase: WorkerDetailsUsecase,
            worker_system_stat: WorkerSystemStat,
            fixt_worker: Worker,
    ):
        await worker_connected_usecase.perform(fixt_worker)
        await worker_system_stat_usecase.perform(
            worker_id=fixt_worker.worker_id,
            system_stat=worker_system_stat
        )

        worker_details = await worker_details_usecase.perform(
            worker_id=fixt_worker.worker_id
        )

        assert worker_details['worker_id'] == fixt_worker.worker_id
        assert worker_details['current_work'] is None
        assert worker_details['system_stats'][0]['cpu'] == {
            'count': 3,
            'load_1': 1.1,
            'load_5': 2.4,
            'load_15': 1.9
        }
        assert worker_details['system_stats'][0]['memory'] == {
            'total': 123,
            'available': 20
        }

    async def test_given_worker_connected_system_stat_when_worker_list_then_at_least_one_should_exist(
            self,
            worker_connected_usecase: WorkerConnectedUsecase,
            worker_system_stat_usecase: WorkerSystemStatUsecase,
            worker_list_usecase: WorkerListUsecase,
            worker_system_stat: WorkerSystemStat,
            fixt_worker: Worker,
    ):
        await worker_connected_usecase.perform(fixt_worker)
        await worker_system_stat_usecase.perform(
            worker_id=fixt_worker.worker_id,
            system_stat=worker_system_stat
        )

        worker_list = await worker_list_usecase.perform()
        assert worker_list[-1]['worker_id'] == fixt_worker.worker_id
        assert worker_list[-1]['last_system_stat']['cpu'] is not None