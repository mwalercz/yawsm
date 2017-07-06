from dq_broker.infrastructure.auth.base import AuthenticationService
from dq_broker.infrastructure.auth.user import UserAuthenticationService, CookieMaker, Validator
from dq_broker.infrastructure.auth.worker import WorkerAuthenticationService


def user_auth(c):
    return UserAuthenticationService(
        cookie_maker=CookieMaker(),
        validator=Validator(),
        ssh_service=c('ssh'),
    )


def worker_auth(c):
    return WorkerAuthenticationService(
        api_key=c('conf')['worker']['api_key']
    )


def auth(c):
    auth = AuthenticationService()
    auth.register(c('user_auth'))
    auth.register(c('worker_auth'))
    return auth


def register(c):
    c.add_service(user_auth)
    c.add_service(worker_auth)
    c.add_service(auth)
