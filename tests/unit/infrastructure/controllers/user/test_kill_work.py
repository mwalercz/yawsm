import asynctest
import pytest

from dq_broker.domain.exceptions import WorkerNotFound
from dq_broker.domain.work.usecases.kill_work import KillWorkUsecase
from dq_broker.infrastructure.controllers.user.kill_work import KillWorkController
from tests.unit.infrastructure.controllers.utils import create_request

pytestmark = pytest.mark.asyncio


class TestKillWorkController:
    async def test_handle_no_error(
            self, mock_user_auth, fixt_username
    ):
        mock_usecase = asynctest.Mock(spec=KillWorkUsecase)
        mock_usecase.perform.return_value = 'some-value'
        controller = KillWorkController(
            usecase=mock_usecase,
            user_auth=mock_user_auth,
        )
        request = create_request(
            message_body={'work_id': 12}
        )
        response = await controller.handle(request)

        assert response.status_code == 200
        assert response.body == 'some-value'

        mock_usecase.perform.assert_called_once_with(
            work_id=12,
            username=fixt_username,
        )

    async def test_handle_when_usecase_raises(
            self, mock_user_auth
    ):
        mock_usecase = asynctest.Mock(spec=KillWorkUsecase)
        mock_usecase.perform.side_effect = WorkerNotFound
        controller = KillWorkController(
            usecase=mock_usecase,
            user_auth=mock_user_auth,
        )
        request = create_request(
            message_body={'work_id': 12}
        )
        response = await controller.handle(request)

        assert response.status_code == 404
