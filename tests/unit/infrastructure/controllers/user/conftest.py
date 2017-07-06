from unittest.mock import Mock

import pytest

from dq_broker.infrastructure.auth.user import UserAuthenticationService


@pytest.fixture
def mock_user_auth(fixt_credentials, fixt_username):
    user_auth = Mock(spec=UserAuthenticationService)
    user_auth.get_credentials.return_value = fixt_credentials
    user_auth.get_username.return_value = fixt_username
    return user_auth