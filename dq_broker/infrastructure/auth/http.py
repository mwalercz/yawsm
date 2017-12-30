import logging
from typing import Dict


from dq_broker.exceptions import UserNotFound
from dq_broker.infrastructure.auth.base import basic_auth_extract_credentials, BasicAuthExtractionFailed
from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.exceptions import AuthenticationFailed
from dq_broker.infrastructure.repositories.user import UserRepository
from dq_broker.user.model import User

log = logging.getLogger(__name__)


class HTTPAuthenticationService:
    def __init__(self, ssh_service: SSHService, user_repo: UserRepository):
        self.ssh_service = ssh_service
        self.user_repo = user_repo

    async def authenticate(self, headers: Dict[str, str]) -> User:
        try:
            credentials = basic_auth_extract_credentials(headers)
        except BasicAuthExtractionFailed as exc:
            raise AuthenticationFailed(str(exc))

        if not await self.ssh_service.try_to_login(
                credentials.username,
                credentials.password
        ):
            raise AuthenticationFailed('Could not login via ssh')

        try:
            user = await self.user_repo.find_by_username(credentials.username)
        except UserNotFound:
            raise AuthenticationFailed('User not found in db')
        else:
            return User(
                user_id=user.user_id,
                username=user.username,
                password=credentials.password,
                is_admin=user.is_admin,
            )




