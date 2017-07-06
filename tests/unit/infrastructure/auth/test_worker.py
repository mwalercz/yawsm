import pytest
from dq_broker.infrastructure.auth.base import Role
from dq_broker.infrastructure.auth.worker import WorkerAuthenticationService

from dq_broker.exceptions import SessionNotFound, AuthenticationFailed


@pytest.fixture
def worker_auth():
    return WorkerAuthenticationService(api_key='123')


@pytest.fixture
def worker_headers():
    return {'x-api-key': '123'}


class TestWorkerAuthentication:
    def test_given_no_peers_then_session_for_peer_should_not_exist(
            self, peer, worker_auth
    ):
        self.assert_session_does_not_exist(peer, worker_auth)

    def test_when_authenticate_with_correct_key_then_session_should_be_created(
            self, peer, worker_auth, worker_headers
    ):
        worker_auth.authenticate(peer, worker_headers)
        assert worker_auth.get_role(peer) == Role.worker

    @pytest.mark.parametrize('param_incorrect_headers', [
        {},
        {'x-api-key': 'incorrect-key'},
        {'api-key': '123'},
    ])
    def test_when_authenticate_with_incorrect_headers_then_it_should_raise(
            self, worker_auth, param_incorrect_headers, peer
    ):
        with pytest.raises(AuthenticationFailed):
            worker_auth.authenticate(peer, param_incorrect_headers)

        self.assert_session_does_not_exist(peer, worker_auth)

    def test_given_worker_in_session_when_remove_then_get_role_should_raise(
            self, peer, worker_auth, worker_headers
    ):
        worker_auth.authenticate(peer, worker_headers)
        worker_auth.remove(peer)

        self.assert_session_does_not_exist(peer, worker_auth)

    def assert_session_does_not_exist(self, peer, worker_auth):
        with pytest.raises(SessionNotFound):
            worker_auth.get_role(peer)
        with pytest.raises(SessionNotFound):
            worker_auth.get_headers(peer)
