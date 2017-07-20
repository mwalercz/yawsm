
from dq_broker.exceptions import AuthenticationFailed


class WorkerAuthenticationService:

    def __init__(self, ssh_service):
        self.ssh_service = ssh_service

    async def authenticate(self, headers):
        try:
            await self._verify(
                headers['username'],
                headers['password'],
            )
            return {}
        except KeyError:
            raise AuthenticationFailed()

    async def _verify(self, username, password):
        if not await self.ssh_service.try_to_login(username, password):
            raise AuthenticationFailed(
                'No such user/password combination.'
            )
        if not self._can_be_worker(username):
            raise AuthenticationFailed(
                'User cannot be worker.'
            )

    def _can_be_worker(self, username):
        return username in ['test', 'mwal']
