from unittest.mock import Mock

import pytest
from dq_broker.infrastructure.auth.worker import WorkerAuthenticationService

from dq_broker.exceptions import AuthenticationFailed
from infrastructure.auth.ssh import SSHService


@pytest.fixture
def mock_ssh():
    ssh = Mock(spec=SSHService)
    ssh.try_to_login.return_value = True
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
    def test_when_authenticate_with_correct_headers_then_no_errors_should_be_raised(
            self, worker_auth, worker_headers
    ):
        worker_auth.authenticate(worker_headers)

    @pytest.mark.parametrize('param_incorrect_headers', [
        {},
        {'username': 'incorrect-key'},
        {'username': '123'},
        {'password': 'some-pass'}
    ])
    def test_when_authenticate_with_incorrect_headers_then_it_should_raise(
            self, worker_auth, param_incorrect_headers
    ):
        with pytest.raises(AuthenticationFailed):
            worker_auth.authenticate(param_incorrect_headers)

    def test_when_ssh_returns_false_then_authenticate_should_raise(
            self, worker_auth, worker_headers, mock_ssh
    ):
        mock_ssh.try_to_login.return_value = False
        with pytest.raises(AuthenticationFailed):
            worker_auth.authenticate(worker_headers)
