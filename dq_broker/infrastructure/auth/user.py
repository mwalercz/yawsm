import logging
from typing import Dict

from dq_broker.exceptions import UserNotFound
from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.exceptions import AuthenticationFailed
from dq_broker.infrastructure.repositories.user import UserRepository
from dq_broker.user.model import User

log = logging.getLogger(__name__)


class UserAuthenticationService:
    def __init__(self, ssh_service: SSHService, user_repo: UserRepository):
        self.ssh_service = ssh_service
        self.user_repo = user_repo

    async def authenticate(self, headers: Dict[str, str]) -> User:
        try:
            return await self._verify_and_get_user_info(
                username=headers['username'],
                password=headers['password'],
            )
        except KeyError:
            raise AuthenticationFailed('username or password not provided')
        except UserNotFound:
            raise AuthenticationFailed(
                'user: "{}" not found in db.'.format(headers['username'])
            )

    async def _verify_and_get_user_info(self, username, password):
        if not await self.ssh_service.try_to_login(username, password):
            raise AuthenticationFailed()
        user = await self.user_repo.find_by_username(username)
        return User(
            user_id=user.user_id,
            username=user.username,
            password=password,
            is_admin=user.is_admin,
        )
