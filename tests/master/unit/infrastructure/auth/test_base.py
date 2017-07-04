import pytest

from ws_dist_queue.master.infrastructure.auth.base import AuthenticationService
from ws_dist_queue.master.infrastructure.auth.user import UserAuthenticationService



@pytest.fixture
def auth(user_auth, worker_auth):
    auth = AuthenticationService()
    auth.register(user_auth)
    auth.register(worker_auth)

