import json

import logging
from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound, HTTPError


log = logging.getLogger(__name__)


def json_error(message, status):
    return web.Response(
        body=json.dumps({'error': message}).encode('utf-8'),
        status=status,
        content_type='application/json'
    )


async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            return await handler(request)
        except HTTPNotFound as exc:
            return json_error('path_not_found', status=404)
        except HTTPError as exc:
            return json_error(exc.reason, status=exc.status_code)

    return middleware_handler
