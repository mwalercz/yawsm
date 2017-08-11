from aiohttp import web
from aiohttp_session import get_session

from dq_broker.exceptions import AuthenticationFailed
from dq_broker.infrastructure.auth.user import UserAuthenticationService


class AuthMiddleware:
    def __init__(self, auth: UserAuthenticationService):
        self.auth = auth

    async def auth_middleware(self, app, handler):
        if getattr(handler, '_auth_required', False) is False:
            return handler

        async def middleware_handler(request):
            session = await get_session(request)
            try:
                user = await self.auth.authenticate(request.headers)
                session['user'] = user.to_dict()
                session.changed()
                return await handler(request)
            except AuthenticationFailed:
                user = session.get('user')
                if user:
                    return await handler(request)
                return web.HTTPUnauthorized()

        return middleware_handler
