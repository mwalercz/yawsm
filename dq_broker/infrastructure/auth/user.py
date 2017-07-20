from dq_broker.exceptions import AuthenticationFailed


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        if not isinstance(other, Credentials):
            return False
        else:
            return (
                self.username == other.username
                and self.password == other.password
            )


class UserAuthenticationService:
    def __init__(self, ssh_service, loop):
        self.ssh_service = ssh_service
        self.loop = loop

    async def authenticate(self, headers):
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
        return {
            'username': username,
            'password': password,
            'is_super_user': self._is_super_user(username)
        }

    def _is_super_user(self, usernamer):
        return False
