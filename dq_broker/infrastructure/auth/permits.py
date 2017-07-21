from aiohttp import web
from aiohttp_session import get_session


def users_must_match(func):
    async def wrapper(self, request):
        param_username = request.match_info['username']
        session = await get_session(request)
        session_username = session['user_info']['username']
        if param_username != session_username:
            return web.HTTPUnauthorized(reason='User {} does not have access to {}'.format(
                session_username,
                param_username,
            ))
        return await func(self, request)

    return wrapper


def auth_required(func):
    func._auth_required = True
    return func
