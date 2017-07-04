from unittest.mock import Mock

import pytest

from ws_dist_queue.master.exceptions import AuthenticationFailed, SessionNotFound
from ws_dist_queue.master.infrastructure.auth.base import Role
from ws_dist_queue.master.infrastructure.auth.ssh import SSHService
from ws_dist_queue.master.infrastructure.auth.user import (
    UserAuthenticationService, CookieMaker, Validator, Credentials,
    UserSession, SecurityInfo
)


@pytest.fixture
def mock_ssh():
    return Mock(spec=SSHService)


@pytest.fixture
def mock_cookie_maker():
    mock_cookie_maker = Mock(spec=CookieMaker)
    mock_cookie_maker.make.side_effect = [
        'some-cookie-1', 'some-cookie-2'
    ]
    return mock_cookie_maker


@pytest.fixture
def mock_validator():
    return Mock(spec=Validator)


@pytest.fixture
def user_auth(mock_ssh, mock_cookie_maker, mock_validator):
    return UserAuthenticationService(
        ssh_service=mock_ssh,
        cookie_maker=mock_cookie_maker,
        validator=mock_validator,
    )


@pytest.fixture
def headers():
    return {
        'username': 'some-user',
        'password': 'some-pass',
        'x-parent-pid': 'parent-pid',
    }


@pytest.fixture
def peer():
    return 'some-peer'


class TestUserAuthService:
    def test_given_ssh_returns_true_when_authenticate_then_session_should_be_created(
            self, user_auth, mock_ssh, headers, peer
    ):
        mock_ssh.try_to_login.return_value = True

        user_auth.authenticate(peer=peer, headers=headers)

        self.assert_session_exists(peer, user_auth)

    def test_given_authenticated_peer_when_remove_peer_then_get_session_should_raise(
            self, user_auth, mock_ssh, headers, peer
    ):
        mock_ssh.try_to_login.return_value = True
        user_auth.authenticate(peer=peer, headers=headers)

        user_auth.remove(peer)

        with pytest.raises(SessionNotFound):
            user_auth.get_session(peer)

    def test_given_peer_in_long_session_when_authenticate_then_session_should_be_restored(
            self, user_auth, mock_ssh, headers, peer, mock_validator
    ):
        mock_ssh.try_to_login.return_value = True
        mock_validator.is_valid.return_value = True
        cookie_headers = {
            'x-cookie': 'some-cookie-1',
            'x-parent-pid': 'parent-pid',
        }
        user_auth.authenticate(peer=peer, headers=headers)
        user_auth.remove(peer)

        user_auth.authenticate(peer=peer, headers=cookie_headers)

        self.assert_session_exists(peer, user_auth)

    def test_given_ssh_returns_false_when_authenticate_then_it_should_raise_error(
            self, user_auth, mock_ssh, headers, peer
    ):
        mock_ssh.try_to_login.return_value = False

        with pytest.raises(AuthenticationFailed):
            user_auth.authenticate(peer=peer, headers=headers)

    def test_authenticate_peer_using_long_session_and_get_role(
            self
    ):
        pass

    def assert_session_exists(self, peer, user_auth):
        credentials = Credentials(
            username='some-user',
            password='some-pass',
        )
        security_info = SecurityInfo(
            cookie='some-cookie-1',
            parent_pid='parent-pid',
        )
        assert user_auth.get_headers(peer) == {'x-cookie': 'some-cookie-1'}
        assert user_auth.get_role(peer) == Role.user
        assert user_auth.get_credentials(peer) == credentials
        assert user_auth.get_session(peer) == UserSession(
            credentials=credentials,
            security_info=security_info,
            role=Role.user,
        )