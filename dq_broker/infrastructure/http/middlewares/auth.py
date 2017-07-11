from aiohttp import web
from aiohttp_session import get_session

from dq_broker.exceptions import AuthenticationFailed


class AuthMiddleware:
    def __init__(self, auth):
        self.auth = auth

    async def auth_middleware(self, app, handler):
        async def middleware_handler(request):
            session = await get_session(request)
            user_info = session.get('user_info')
            if user_info:
                return await handler(request)
            try:
                session['user_info'] = self.auth.authenticate(request.headers)
                session.changed()
                return await handler(request)
            except AuthenticationFailed:
                return web.HTTPForbidden()

        return middleware_handler
