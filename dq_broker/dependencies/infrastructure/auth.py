from dq_broker.infrastructure.auth.user import UserAuthenticationService
from dq_broker.infrastructure.auth.worker import WorkerAuthenticationService


def user_auth(c):
    return UserAuthenticationService(
        ssh_service=c('ssh'),
        user_repo=c('user_repo'),
    )


def worker_auth(c):
    return WorkerAuthenticationService(
        ssh_service=c('ssh')
    )


def register(c):
    c.add_service(user_auth)
    c.add_service(worker_auth)
