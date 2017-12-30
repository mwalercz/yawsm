from dq_broker.infrastructure.auth.http import HTTPAuthenticationService
from dq_broker.infrastructure.auth.ws import WebSocketAuthenticationService


def user_auth(c):
    return HTTPAuthenticationService(
        ssh_service=c('ssh'),
        user_repo=c('user_repo'),
    )


def worker_auth(c):
    return WebSocketAuthenticationService(
        ssh_service=c('ssh')
    )


def register(c):
    c.add_service(user_auth)
    c.add_service(worker_auth)
