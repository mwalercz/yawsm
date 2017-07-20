import functools
import paramiko
from paramiko import SSHClient, SSHException


class SSHService:
    def __init__(self, hostname, loop):
        self.hostname = hostname
        self.loop = loop

    async def try_to_login(self, username, password):
        return await self.loop.run_in_executor(
            executor=None,
            func=functools.partial(self._try_to_login, username, password)
        )

    def _try_to_login(self, username, password):
        with SSHClient() as client:
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            try:
                client.connect(
                    hostname=self.hostname,
                    username=username,
                    password=password,
                )
                return True
            except SSHException:
                return False
