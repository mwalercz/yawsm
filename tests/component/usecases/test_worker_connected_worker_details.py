import pytest

from dq_broker.domain.worker.model import Worker, SystemStat
from dq_broker.domain.worker.usecases.details import WorkerDetailsUsecase
from dq_broker.domain.worker.usecases.list import WorkerListUsecase
from dq_broker.domain.worker.usecases.worker_connected import WorkerConnectedUsecase
from dq_broker.domain.worker.usecases.worker_system_stat import WorkerSystemStatUsecase


pytestmark = pytest.mark.asyncio


class TestConnectedWorkerShouldBeReturnedInDetailsAndList:
    async def test_given_worker_connected_system_stat_when_worker_details_then_it_should_exist(
            self,
            worker_connected_usecase: WorkerConnectedUsecase,
            worker_system_stat_usecase: WorkerSystemStatUsecase,
            worker_details_usecase: WorkerDetailsUsecase,
            worker_system_stat: SystemStat,
            fixt_new_worker_dto: Worker,
    ):
        await worker_connected_usecase.perform(fixt_new_worker_dto)
        await worker_system_stat_usecase.perform(
            worker_socket=fixt_new_worker_dto.worker_socket,
            system_stat=worker_system_stat
        )

        worker_details = await worker_details_usecase.perform(
            worker_socket=fixt_new_worker_dto.worker_socket
        )

        assert worker_details['worker_socket'] == fixt_new_worker_dto.worker_socket
        assert worker_details['current_work'] is None
        assert worker_details['system_stats'][0]['load_15'] == 1.9
        assert worker_details['system_stats'][0]['available_memory'] == 20

    async def test_given_worker_connected_system_stat_when_worker_list_then_at_least_one_should_exist(
            self,
            worker_connected_usecase: WorkerConnectedUsecase,
            worker_system_stat_usecase: WorkerSystemStatUsecase,
            worker_list_usecase: WorkerListUsecase,
            worker_system_stat: SystemStat,
            fixt_new_worker_dto: Worker,
    ):
        await worker_connected_usecase.perform(fixt_new_worker_dto)
        await worker_system_stat_usecase.perform(
            worker_socket=fixt_new_worker_dto.worker_socket,
            system_stat=worker_system_stat
        )

        worker_list = await worker_list_usecase.perform()
        assert worker_list[-1]['worker_socket'] == fixt_new_worker_dto.worker_socket
        assert worker_list[-1]['last_system_stat']['load_15'] is not None