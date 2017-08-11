from unittest.mock import Mock, ANY

import pytest

from dq_broker.exceptions import AccessForbidden
from dq_broker.infrastructure.http.controllers.schema import WorkIdSchema
from dq_broker.infrastructure.websocket.clients import ResponseClient
from dq_broker.infrastructure.websocket.message import IncomingMessage
from dq_broker.infrastructure.websocket.request import Response, validate
from dq_broker.infrastructure.websocket.routing import Route, Router
from dq_broker.infrastructure.websocket.supervisor import Supervisor

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_sender():
    return Mock()


@pytest.fixture
def mock_response_client():
    return Mock(spec=ResponseClient)


@pytest.fixture
def mock_router():
    return Mock(spec=Router)


@pytest.fixture
async def supervisor(mock_response_client, mock_router):
    return Supervisor(
        response_client=mock_response_client,
        router=mock_router,
    )


class ReturningController:
    async def handle(self, req):
        return req.get_response(
            status_code=202,
            body={'req_body': req.message.body}
        )


class NotReturningController:
    async def handle(self, req):
        pass


class ExceptionRaisingController:
    async def handle(self, req):
        raise KeyError('not found')


class ValidationErrorRaisingController:
    @validate(schema=WorkIdSchema)
    def handle(self, req):
        pass


class TestSupervisor:
    PATH = 'some_path'
    PEER = '123.123.1.1:134'

    async def test_when_controller_returns_response_then_response_should_be_sent(
            self, mock_sender, mock_router, mock_response_client, supervisor
    ):
        message_body = {'key': 'cool_stuff'}
        mock_router.get_route.return_value = self.get_route(ReturningController())
        message = self.get_message(message_body)

        await supervisor.handle_message(
            sender=mock_sender,
            peer=self.PEER,
            message=message
        )

        mock_response_client.send.assert_called_once_with(
            recipient=mock_sender,
            response=Response(
                path=self.PATH,
                status_code=202,
                body={'req_body': message_body},
            )
        )
        mock_router.get_route.assert_called_once_with(
            message.path,
        )

    async def test_when_controller_returns_nothing_then_nothing_should_be_sent(
            self, mock_sender, mock_router, supervisor, mock_response_client
    ):
        mock_router.get_route.return_value = self.get_route(NotReturningController())
        message = self.get_message()

        await supervisor.handle_message(mock_sender, self.PEER, message)

        mock_response_client.send.assert_not_called()

    async def test_when_controller_raises_exception_then_error_response_should_be_sent(
            self, mock_sender, mock_router, supervisor, mock_response_client
    ):
        mock_router.get_route.return_value = self.get_route(ExceptionRaisingController())
        message = self.get_message()

        await supervisor.handle_message(mock_sender, self.PEER, message)

        mock_response_client.send.assert_called_once_with(
            recipient=mock_sender,
            response=Response(
                path=self.PATH,
                status_code=500,
                body=ANY,
            )
        )

    async def test_when_validation_error_is_raised_then_error_response_should_be_sent(
            self, mock_sender, mock_router, supervisor, mock_response_client
    ):
        mock_router.get_route.return_value = self.get_route(ValidationErrorRaisingController())
        message = self.get_message()
        expected_error = {
            'work_id': ['This field is required.'],
        }

        await supervisor.handle_message(mock_sender, self.PEER, message)

        mock_response_client.send.assert_called_once_with(
            recipient=mock_sender,
            response=Response(
                path=self.PATH,
                status_code=400,
                body={'error': expected_error}
            )
        )

    async def test_when_router_raises_access_forbidden_then_error_response_should_be_sent(
            self, mock_sender, mock_router, supervisor, mock_response_client
    ):
        msg = 'access is forbidden'
        mock_router.get_route.side_effect = AccessForbidden(data=msg)
        message = self.get_message()

        await supervisor.handle_message(mock_sender, self.PEER, message)

        mock_response_client.send.assert_called_once_with(
            recipient=mock_sender,
            response=Response(
                path=self.PATH,
                status_code=403,
                body={'error': msg}
            )
        )

    def get_route(self, controller):
        return Route(
            path=self.PATH,
            controller=controller,
        )

    def get_message(self, message_body=None):
        return IncomingMessage(
            path=self.PATH,
            body=message_body
        )
