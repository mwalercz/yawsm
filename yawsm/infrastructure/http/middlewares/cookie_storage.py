import logging

import time

from aiohttp_session import Session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

log = logging.getLogger(__name__)


class EncryptedCookieStorageWithMaxAgeExpiration(
    EncryptedCookieStorage
):
    async def load_session(self, request):
        session = await super(
            EncryptedCookieStorageWithMaxAgeExpiration, self
        ).load_session(request)
        if (
            self.max_age and
            session.new is False and
            session.created + self.max_age < int(time.time())
        ):
            log.warning('Cookie expired, '
                        'create a new fresh session')
            return Session(None, data=None,
                           new=True, max_age=self.max_age)
        return session
