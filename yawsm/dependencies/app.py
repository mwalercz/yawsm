import asyncio
from configparser import SafeConfigParser

import os

from yawsm.dependencies.domain.services import (
    register as register_domain
)
from yawsm.dependencies.domain.usecases.work import (
    register as register_work_usecases
)
from yawsm.dependencies.domain.usecases.user import (
    register as register_user_usecases
)
from yawsm.dependencies.domain.usecases.worker import (
    register as register_worker_usecases
)
from yawsm.dependencies.infrastructure.auth import (
    register as register_auth
)
from yawsm.dependencies.infrastructure.db import (
    register as register_db,
)
from yawsm.dependencies.infrastructure.http.controllers import (
    register as register_http_controllers
)
from yawsm.dependencies.infrastructure.http.routing import (
    register_http_routing
)
from yawsm.dependencies.infrastructure.http.services import (
    register as register_http_services
)
from yawsm.dependencies.infrastructure.serialization import (
    register as register_serialization
)
from yawsm.dependencies.infrastructure.websocket.clients import (
    register as register_clients
)
from yawsm.dependencies.infrastructure.websocket.controllers import (
    register as register_ws_controllers
)
from yawsm.dependencies.infrastructure.websocket.routing import register_ws_routing
from yawsm.dependencies.infrastructure.websocket.services import (
    register as register_ws_services
)
from yawsm.infrastructure.auth.ssh import SSHService
from yawsm.infrastructure.loop_policy import StrictEventLoopPolicy


def conf(c):
    conf = SafeConfigParser(os.environ)
    conf.read(c('config_path'))
    return conf


def loop(c):
    asyncio.set_event_loop_policy(StrictEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    return loop


def ssh(c):
    return SSHService(
        hostname=c('conf')['ssh']['host'],
    )


def register_usecases(c):
    register_worker_usecases(c)
    register_work_usecases(c)
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
