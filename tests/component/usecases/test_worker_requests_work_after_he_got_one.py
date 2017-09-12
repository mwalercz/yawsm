from unittest.mock import sentinel

import pytest

from dq_broker.domain.worker.model import Worker

pytestmark = pytest.mark.asyncio


@pytest.mark.skip(
    reason='we are notifying only free workers, '
           'so this situation should not happen'
)
class TestCreateAndFinishWork:
    async def test_create_and_finish_work(
            self, fixt_new_work, fixt_worker, fixt_user,
            new_work_usecase,
            worker_connected_usecase,
            worker_requests_work_usecase,
            worker_client
    ):
        await new_work_usecase.perform(fixt_new_work, fixt_user)
        work_2_id = await new_work_usecase.perform(fixt_new_work, fixt_user)
        await worker_connected_usecase.perform(fixt_worker)
        await worker_requests_work_usecase.perform(fixt_worker.worker_socket)
        before_work_to_be_done_call_count = self._get_work_to_be_done_call_count(worker_client)
        await worker_requests_work_usecase.perform(fixt_worker.worker_socket)
        assert before_work_to_be_done_call_count == self._get_work_to_be_done_call_count(worker_client)

        worker_2 = Worker(
            worker_socket='1.2.3.4:91911',
            worker_ref=sentinel.worker_2_ref
        )
        await worker_connected_usecase.perform(worker_2)
        await worker_requests_work_usecase.perform(worker_2.worker_socket)
        worker_client.send.assert_called_with(
            action_name='work_to_be_done',
            recipient=sentinel.worker_2_ref,
            body={
                'work_id': work_2_id,
                'cwd': fixt_new_work.cwd,
                'command': fixt_new_work.command,
                'env': fixt_new_work.env,
                'username': fixt_user.username,
                'password': fixt_user.password,
            }
        )

    def _get_work_to_be_done_call_count(self, worker_client):
        return len([
            call for call in worker_client.send.call_args_list
            if call[1]['action_name'] == 'work_to_be_done'
        ])

