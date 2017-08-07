from aiohttp import web
from aiohttp_session import get_session


def users_must_match(func):
    async def wrapper(self, request):
        param_username = request.match_info['username']
        session = await get_session(request)
        if (
                session['user_info']['is_admin']
                or session['user_info']['username'] == param_username
        ):
            return await func(self, request)
        else:
            return web.HTTPUnauthorized(
                reason='User {} does not have access to {} resources'.format(
                    session['user_info']['username'],
                    param_username,
                ))

    return wrapper


def admin_only(func):
    async def wrapper(self, request):
        session = await get_session(request)
        if session['user_info']['is_admin']:
            return await func(self, request)
        else:
            return web.HTTPUnauthorized(
                reason='User {} is not super_user'.format(
                    session['user_info']['username']
                ))

    return wrapper


def auth_required(func):
    func._auth_required = True
    return func
