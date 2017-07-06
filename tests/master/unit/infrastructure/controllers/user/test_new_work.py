import asynctest
import pytest

from tests.master.unit.infrastructure.controllers.utils import create_request
from ws_dist_queue.master.domain.work.model import Work, CommandData
from ws_dist_queue.master.domain.work.usecases.new_work import NewWorkUsecase
from ws_dist_queue.master.infrastructure.controllers.user.new_work import NewWorkController

pytestmark = pytest.mark.asyncio


class TestNewWorkController:
    async def test_handle(self, fixt_credentials, mock_user_auth):
        mock_usecase = asynctest.Mock(spec=NewWorkUsecase)
        mock_usecase.perform.side_effect = [1, 2, 3]
        controller = NewWorkController(
            usecase=mock_usecase,
            user_auth=mock_user_auth,
        )
        request = create_request(
            message_body={
                'command': 'some-command',
                'cwd': '/home',
            }
        )

        response = await controller.handle(request)

        assert response.status_code == 202
        assert response.body['work_id'] == 1
        mock_usecase.perform.assert_called_once_with(
            Work(
                work_id=None,
                command_data=CommandData(
                    command='some-command',
                    cwd='/home',
                    env={},
                ),
                credentials=fixt_credentials,
            )
        )
