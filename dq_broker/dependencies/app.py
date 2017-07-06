import asyncio
from configparser import ConfigParser

from dq_broker.dependencies.domain.services import (
    register as register_domain_services
)
from dq_broker.dependencies.domain.usecases.work import (
    register as register_user_usecases
)
from dq_broker.dependencies.domain.usecases.worker import (
    register as register_worker_usecases
)
from dq_broker.dependencies.infrastructure.auth import (
    register as register_auth
)
from dq_broker.dependencies.infrastructure.clients import (
    register as register_clients
)
from dq_broker.dependencies.infrastructure.controllers.default import (
    register as register_default_controller
)
from dq_broker.dependencies.infrastructure.controllers.user import (
    register as register_user_controllers
)
from dq_broker.dependencies.infrastructure.controllers.worker import (
    register as register_worker_controllers
)
from dq_broker.dependencies.infrastructure.db import (
    register as register_db_services
)
from dq_broker.dependencies.infrastructure.services import (
    register as register_infra_services
)
from dq_broker.dependencies.infrastructure.ws import (
    register as register_ws_services
)
from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.infrastructure.loop_policy import StrictEventLoopPolicy

from dq_broker.dependencies.routing import register_routing


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def loop(c):
    asyncio.set_event_loop_policy(StrictEventLoopPolicy())
    return asyncio.get_event_loop()


def ssh(c):
    return SSHService(
        hostname=c('conf')['ssh']['hostname']
    )


def register_usecases(c):
    register_worker_usecases(c)
    register_user_usecases(c)


def register_controllers(c):
    register_default_controller(c)
    register_user_controllers(c)
    register_worker_controllers(c)
    register_routing(
        r=c('router'),
        c=c,
    )


def register_app(c):
    c.add_service(conf)
    c.add_service(loop)

    register_clients(c)
    register_db_services(c)
    register_domain_services(c)
    register_infra_services(c)

    register_usecases(c)

    c.add_service(ssh)
    register_auth(c)

    register_controllers(c)

    register_ws_services(c)
