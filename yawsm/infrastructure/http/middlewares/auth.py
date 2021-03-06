from aiohttp import web
from aiohttp_session import get_session

from yawsm.infrastructure.auth.http import HTTPAuthenticationService
from yawsm.infrastructure.exceptions import AuthenticationFailed


class AuthMiddleware:
    def __init__(self, auth: HTTPAuthenticationService):
        self.auth = auth

    async def auth_middleware(self, app, handler):
        if getattr(handler, '_auth_required', False) is False:
            return handler

        async def middleware_handler(request):
            session = await get_session(request)
            user = session.get('user')
            if user:
                return await handler(request)
            try:
                user = await self.auth.authenticate(request.headers)
                session['user'] = user._asdict()
                session.changed()
                return await handler(request)
            except AuthenticationFailed as exc:
                return web.HTTPUnauthorized(
                    headers={'WWW-Authenticate': 'Basic'},
                    reason=str(exc)
                )

        return middleware_handler
