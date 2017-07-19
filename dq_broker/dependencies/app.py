import asyncio
from configparser import ConfigParser

from dq_broker.dependencies.infrastructure.websocket.controllers import (
    register as register_ws_controllers
)

from dq_broker.dependencies.infrastructure.websocket.clients import (
    register as register_clients
)
from dq_broker.dependencies.infrastructure.websocket.services import (
    register as register_ws_services
)
from dq_broker.dependencies.infrastructure.websocket.routing import register_ws_routing
from dq_broker.dependencies.domain.services import (
    register as register_domain
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
from dq_broker.dependencies.infrastructure.db import (
    register as register_db
)
from dq_broker.dependencies.infrastructure.serialization import (
    register as register_serialization
)
from dq_broker.dependencies.infrastructure.http.controllers import (
    register as register_http_controllers
)
from dq_broker.dependencies.infrastructure.http.services import (
    register as register_http_services
)
from dq_broker.dependencies.infrastructure.http.routing import (
    register_http_routing
)


from dq_broker.infrastructure.auth.ssh import SSHService
from dq_broker.lib.loop_policy import StrictEventLoopPolicy


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def loop(c):
    asyncio.set_event_loop_policy(StrictEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    return loop


def ssh(c):
    return SSHService(
        hostname=c('conf')['ssh']['hostname']
    )


def register_usecases(c):
    register_worker_usecases(c)
    register_user_usecases(c)


def register_ws(c):
    register_ws_services(c)
    register_ws_controllers(c)
    register_ws_routing(
        r=c('router'),
        c=c,
    )


def register_http(c):
    register_http_services(c)
    register_http_controllers(c)
    register_http_routing(
        r=c('http_router'),
        c=c
    )



def register_all(c):
    c.add_service(conf)
    c.add_service(loop)

    register_serialization(c)
    register_clients(c)
    register_db(c)
    register_domain(c)

    register_usecases(c)

    c.add_service(ssh)
    register_auth(c)

    register_ws(c)
    register_http(c)
