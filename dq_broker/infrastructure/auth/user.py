import logging
from typing import Dict, NamedTuple

from dq_broker.domain.user.model import User
from dq_broker.exceptions import AuthenticationFailed
from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.repositories.user import UserRepository

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
            raise AuthenticationFailed()

    async def _verify_and_get_user_info(self, username, password):
        if not await self.ssh_service.try_to_login(username, password):
            raise AuthenticationFailed()
        user, was_created = await self.user_repo.get_or_create(username)
        if was_created:
            log.info('New user was created: {}'.format(user.username))
        return User(
            user_id=user.user_id,
            username=user.username,
            password=password,
            is_admin=user.is_admin,
        )
