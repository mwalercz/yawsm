from unittest.mock import Mock

import pytest
from dq_broker.infrastructure.auth.base import Role
from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.auth.user import (
    UserAuthenticationService, CookieMaker, Validator, Credentials,
    UserSession, SecurityInfo
)

from dq_broker.exceptions import AuthenticationFailed, SessionNotFound


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


class TestUserAuthService:

    def test_given_ssh_returns_false_when_authenticate_then_it_should_raise_error(
            self, user_auth, mock_ssh, user_headers, peer
    ):
        mock_ssh.try_to_login.return_value = False

        with pytest.raises(AuthenticationFailed):
            user_auth.authenticate(peer=peer, headers=user_headers)

    def test_given_no_sessions_when_get_session_then_get_session_should_raise(
            self, user_auth, peer,
    ):
        with pytest.raises(SessionNotFound):
            user_auth.get_session(peer=peer)

    def test_given_ssh_returns_true_when_authenticate_then_session_should_be_created(
            self, user_auth, mock_ssh, user_headers, peer
    ):
        mock_ssh.try_to_login.return_value = True

        user_auth.authenticate(peer=peer, headers=user_headers)

        self.assert_session_exists_and_is_correct(peer, user_auth)

    def test_given_authenticated_peer_when_remove_peer_then_get_session_should_raise(
            self, user_auth, mock_ssh, user_headers, peer
    ):
        mock_ssh.try_to_login.return_value = True
        user_auth.authenticate(peer=peer, headers=user_headers)

        user_auth.remove(peer)

        with pytest.raises(SessionNotFound):
            user_auth.get_session(peer)

    def test_given_peer_in_long_session_when_authenticate_then_session_should_be_restored(
            self, user_auth, mock_ssh, user_headers, peer, mock_validator, cookie_headers
    ):
        mock_ssh.try_to_login.return_value = True
        mock_validator.is_valid.return_value = True
        user_auth.authenticate(peer=peer, headers=user_headers)
        user_auth.remove(peer)

        user_auth.authenticate(peer=peer, headers=cookie_headers)

        self.assert_session_exists_and_is_correct(peer, user_auth)

    def test_given_peer_in_long_session_when_authenticate_with_invalid_cookie_then_auth_should_raise(
            self, user_auth, mock_ssh, user_headers, peer, mock_validator, cookie_headers
    ):
        mock_ssh.try_to_login.return_value = True
        mock_validator.is_valid.return_value = False
        user_auth.authenticate(peer=peer, headers=user_headers)
        user_auth.remove(peer)

        with pytest.raises(AuthenticationFailed):
            user_auth.authenticate(peer=peer, headers=cookie_headers)

    def test_given_two_authenticated_peers_when_get_session_then_peer_1_session_should_be_returned(
            self, peer, user_headers, user_auth
    ):
        other_peer = 'other-peer'
        user_auth.authenticate(peer=peer, headers=user_headers)
        user_auth.authenticate(peer=other_peer, headers=user_headers)

        self.assert_session_exists_and_is_correct(peer, user_auth)
        self.assert_session_exists_and_is_correct(
            other_peer, user_auth, cookie='some-cookie-2'
        )

    def assert_session_exists_and_is_correct(
            self, peer, user_auth, cookie='some-cookie-1'
    ):
        credentials = Credentials(
            username='some-user',
            password='some-pass',
        )
        security_info = SecurityInfo(
            cookie=cookie,
            parent_pid='parent-pid',
        )
        assert user_auth.get_headers(peer) == {'x-cookie': cookie}
        assert user_auth.get_role(peer) == Role.user
        assert user_auth.get_credentials(peer) == credentials
        assert user_auth.get_session(peer) == UserSession(
            credentials=credentials,
            security_info=security_info,
            role=Role.user,
        )
