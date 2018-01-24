from yawsm.infrastructure.auth.base import basic_auth_extract_credentials, BasicAuthExtractionFailed
from yawsm.infrastructure.exceptions import AuthenticationFailed


class WebSocketAuthenticationService:
    def __init__(self, ssh_service):
        self.ssh_service = ssh_service

    async def authenticate(self, headers):
        try:
            credentials = basic_auth_extract_credentials(headers)
        except BasicAuthExtractionFailed as exc:
            raise AuthenticationFailed(str(exc))

        if not await self.ssh_service.try_to_login(
            credentials.username, credentials.password
        ):
            raise AuthenticationFailed('No such work/password combination.')

        if not await self._can_be_worker(credentials.username):
            raise AuthenticationFailed('User {} cannot be worker.'.format(credentials.username))

    async def _can_be_worker(self, username):
        return username in ['test', 'mwal']
