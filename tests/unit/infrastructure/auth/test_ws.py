import asyncio
from unittest.mock import Mock

import base64
import pytest

from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.auth.ws import WebSocketAuthenticationService
from dq_broker.infrastructure.exceptions import AuthenticationFailed

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
def ws_auth(mock_ssh):
    return WebSocketAuthenticationService(ssh_service=mock_ssh)


class TestWorkerAuthentication:

    @pytest.mark.parametrize('param_headers', [
        {'authorization': ' '.join(['Basic', base64.b64encode(b'test:pasword').decode()])},
        {'authorization': 'Basic dGVzdDpwYXNzd29yZA=='}
    ])
    async def test_when_authenticate_with_correct_headers_then_no_errors_should_be_raised(
            self, ws_auth, param_headers
    ):
        await ws_auth.authenticate(param_headers)

    @pytest.mark.parametrize('param_incorrect_headers', [
        {},
        {'authorization': ''},
        {'authorization': 'Basic'},
        {'authorization': 'Basic not-encoded'}
    ])
    async def test_when_authenticate_with_incorrect_headers_then_it_should_raise(
            self, ws_auth, param_incorrect_headers
    ):
        with pytest.raises(AuthenticationFailed):
            await ws_auth.authenticate(param_incorrect_headers)

    async def test_when_ssh_returns_false_then_authenticate_should_raise(
            self, ws_auth, mock_ssh
    ):
        headers = {'authorization': 'Basic dGVzdDpwYXNzd29yZA=='}
        mock_ssh._try_to_login.return_value = False
        with pytest.raises(AuthenticationFailed):
            await ws_auth.authenticate(headers)
