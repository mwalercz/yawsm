import logging

import asyncssh

log = logging.getLogger(__name__)


class SSHService:
    def __init__(self, hostname):
        self.hostname = hostname

    async def try_to_login(self, username, password):
        try:
            await asyncssh.create_connection(
                None,
                self.hostname,
                known_hosts=None,
                username=username,
                password=password,
            )
            return True
        except (OSError, asyncssh.Error) as exc:
            log.info('Could not authenticate user %s via SSH %s', username, str(exc))
            return False
