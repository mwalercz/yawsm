from unittest.mock import Mock

import pytest

from ws_dist_queue.master.infrastructure.clients import ResponseClient
from ws_dist_queue.master.infrastructure.controllers.supervisor import Supervisor
from ws_dist_queue.master.infrastructure.executor import Executor
from ws_dist_queue.master.infrastructure.request import Request, Response
from ws_dist_queue.master.infrastructure.routing import Route
from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import WorkIdSchema

pytestmark = pytest.mark.asyncio


class ReturningController:
    def handle(self, req):
        return req.get_response(
            status_code=202,
            body={'req_body': req.message['body']}
        )


class NotReturningController:
    def handle(self, req):
        pass


class ExceptionRaisingController:
    def handle(self, req):
        raise KeyError('not found')


class ValidationErrorRaisingController:
    @validate(schema=WorkIdSchema)
    def handle(self, req):
        pass


@pytest.fixture
def mock_sender():
    return Mock()


@pytest.fixture
def mock_response_client():
    return Mock(spec=ResponseClient)


@pytest.fixture
async def supervisor(mock_response_client):
    return Supervisor(
        executor=Executor(),
        response_client=mock_response_client,
    )


class TestSupervisor:
    PATH = 'some_path'
    PEER = '123.123.1.1:134'

    async def test_when_controller_returns_response_then_response_should_be_sent(
            self, mock_sender, mock_response_client, supervisor
    ):
        message_body = {'key': 'cool_stuff'}
        route = self.get_route(ReturningController())
        request = self.get_request(mock_sender, route, message_body=message_body)

        await supervisor.handle_request(request, route)

        mock_response_client.send.assert_called_with(
            recipient=mock_sender,
            response=Response(
                path=self.PATH,
                status_code=202,
                body={'req_body': message_body},
            )
        )

    async def test_when_controller_returns_nothing_then_nothing_should_be_sent(
            self, mock_sender, supervisor, mock_response_client
    ):
        route = self.get_route(NotReturningController())
        request = self.get_request(mock_sender, route)

        await supervisor.handle_request(request, route)

        mock_response_client.send.assert_not_called()

    async def test_when_controller_raises_exception_then_error_response_should_be_returned(
            self, mock_sender, supervisor, mock_response_client
    ):
        route = self.get_route(ExceptionRaisingController())
        request = self.get_request(mock_sender, route)

        await supervisor.handle_request(request, route)

        mock_response_client.send.assert_called_with(
            recipient=mock_sender,
            response=Response(
                path=self.PATH,
                status_code=500,
            )
        )

    async def test_when_validation_error_is_raised_then_error_response_should_be_returned(
            self, mock_sender, supervisor, mock_response_client
    ):
        route = self.get_route(ValidationErrorRaisingController())
        request = self.get_request(mock_sender, route)
        data = {
            'work_id': ['This field is required.'],
        }

        await supervisor.handle_request(request, route)

        mock_response_client.send.assert_called_with(
            recipient=mock_sender,
            response=Response(
                path=self.PATH,
                status_code=400,
                body={'error': data}
            )
        )

    def get_route(self, controller):
        return Route(
            path=self.PATH,
            controller=controller,
            role=Mock()
        )

    def get_request(self, mock_sender, route, message_body=None):
        return Request(
            message={
                'headers': {
                    'path': self.PATH
                },
                'body': message_body or {},
            },
            sender=mock_sender,
            peer=self.PEER,
            route=route,
        )
