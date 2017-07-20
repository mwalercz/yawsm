from unittest.mock import Mock

import asyncio
import pytest
from dq_broker.infrastructure.auth.worker import WorkerAuthenticationService

from dq_broker.exceptions import AuthenticationFailed
from infrastructure.auth.ssh import SSHService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_ssh():
    ssh = SSHService(
        hostname='some-hostname',
        loop=asyncio.get_event_loop()
    )
    ssh._try_to_login = Mock(return_value=True)
    return ssh


@pytest.fixture
def worker_auth(mock_ssh):
    return WorkerAuthenticationService(ssh_service=mock_ssh)


@pytest.fixture
def worker_headers():
    return {
        'username': 'test',
        'password': 'test'
    }


class TestWorkerAuthentication:
    async def test_when_authenticate_with_correct_headers_then_no_errors_should_be_raised(
            self, worker_auth, worker_headers
    ):
        await worker_auth.authenticate(worker_headers)

    @pytest.mark.parametrize('param_incorrect_headers', [
        {},
        {'username': 'incorrect-key'},
        {'username': '123'},
        {'password': 'some-pass'}
    ])
    async def test_when_authenticate_with_incorrect_headers_then_it_should_raise(
            self, worker_auth, param_incorrect_headers
    ):
        with pytest.raises(AuthenticationFailed):
            await worker_auth.authenticate(param_incorrect_headers)

    async def test_when_ssh_returns_false_then_authenticate_should_raise(
            self, worker_auth, worker_headers, mock_ssh
    ):
        mock_ssh._try_to_login.return_value = False
        with pytest.raises(AuthenticationFailed):
            await worker_auth.authenticate(worker_headers)
