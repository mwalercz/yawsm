from unittest.mock import Mock

import pytest

from ws_dist_queue.master.exceptions import AuthenticationFailed
from ws_dist_queue.master.infrastructure.auth.base import AuthenticationService
from ws_dist_queue.master.infrastructure.auth.user import UserAuthenticationService
from ws_dist_queue.master.infrastructure.auth.worker import WorkerAuthenticationService


@pytest.fixture
def mock_user_auth():
    return Mock(spec=UserAuthenticationService)


@pytest.fixture
def mock_worker_auth():
    return Mock(spec=WorkerAuthenticationService)


@pytest.fixture
def auth(mock_worker_auth, mock_user_auth):
    auth = AuthenticationService()
    auth.register(mock_worker_auth)
    auth.register(mock_user_auth)
    return auth


class TestAuthSerice:
    def test_authenticate_1(
            self, auth, mock_worker_auth, peer
    ):
        mock_worker_auth.authenticate.side_effect = AuthenticationFailed()
        headers = {}

        auth.authenticate(peer, headers)

    def test_authenticate_2(
            self, auth, mock_user_auth, mock_worker_auth, peer
    ):
        mock_worker_auth.authenticate.side_effect = AuthenticationFailed()
        mock_user_auth.authenticate.side_effect = AuthenticationFailed()
        headers = {}

        with pytest.raises(AuthenticationFailed):
            auth.authenticate(peer, headers)

