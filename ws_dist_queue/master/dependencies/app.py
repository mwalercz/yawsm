from configparser import ConfigParser

from ws_dist_queue.master.dependencies.infrastructure.services import (
    register as register_infra_services
)
from ws_dist_queue.master.dependencies.infrastructure.db import (
    register as register_db_services
)
from ws_dist_queue.master.dependencies.infrastructure.ws import (
    register as register_ws_services
)
from ws_dist_queue.master.dependencies.domain.services import (
    register as register_domain_services
)
from ws_dist_queue.master.dependencies.infrastructure.controllers.worker import (
    register as register_worker_controllers
)
from ws_dist_queue.master.dependencies.infrastructure.controllers.user import (
    register as register_user_controllers
)
from ws_dist_queue.master.dependencies.domain.usecases.work import (
    register as register_user_usecases
)
from ws_dist_queue.master.dependencies.domain.usecases.worker import (
    register as register_worker_usecases
)
from ws_dist_queue.master.dependencies.infrastructure.clients import (
    register as register_clients
)
from ws_dist_queue.master.dependencies.routing import register_routing


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def register_domain(c):
    c.add_service(conf)

    register_infra_services(c)
    register_db_services(c)
    register_domain_services(c)

    register_worker_usecases(c)
    register_user_usecases(c)


def register_ws(c):
    register_clients(c)
    register_ws_services(c)
    register_user_controllers(c)
    register_worker_controllers(c)
    register_routing(
        r=c('router'),
        c=c,
    )


def register_app(c):
    register_domain(c)
    register_ws(c)
