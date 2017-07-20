from aiohttp import web
from aiohttp_session import get_session

from dq_broker.exceptions import AuthenticationFailed


class AuthMiddleware:
    def __init__(self, auth):
        self.auth = auth

    async def auth_middleware(self, app, handler):
        async def middleware_handler(request):
            session = await get_session(request)
            try:
                user_info = await self.auth.authenticate(request.headers)
            except AuthenticationFailed:
                user_info = session.get('user_info')
                if user_info:
                    return await handler(request)
                return web.HTTPUnauthorized()
            else:
                session['user_info'] = user_info
                session.changed()
                return await handler(request)

        return middleware_handler
