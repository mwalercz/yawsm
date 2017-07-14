from base64 import urlsafe_b64decode

from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography.fernet import Fernet

from infrastructure.http.middlewares.auth import AuthMiddleware
from infrastructure.http.middlewares.error import error_middleware


def http_router(c):
    return UrlDispatcher()


def http_app(c):
    return web.Application(
        router=c('http_router'),
        middlewares=[
            error_middleware,
            session_middleware(
                EncryptedCookieStorage(
                    secret_key=urlsafe_b64decode(Fernet.generate_key()),
                    max_age=120,
                    cookie_name='DQ_SESSION'
                )),
            AuthMiddleware(c('user_auth')).auth_middleware,
        ]
    )


def register(c):
    c.add_service(http_router)
    c.add_service(http_app)
