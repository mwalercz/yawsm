from dq_broker.infrastructure.auth.base import AuthenticationService
from dq_broker.infrastructure.auth.user import UserAuthenticationService
from dq_broker.infrastructure.auth.worker import WorkerAuthenticationService


def user_auth(c):
    return UserAuthenticationService(
        ssh_service=c('ssh'),
    )


def worker_auth(c):
    return WorkerAuthenticationService(
        api_key=c('conf')['worker']['api_key']
    )


def register(c):
    c.add_service(user_auth)
    c.add_service(worker_auth)
