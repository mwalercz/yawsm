from dq_broker.infrastructure.auth.base import WORKER_ROLES
from infrastructure.websocket.routing import Route as _


def register_ws_routing(r, c):
    r.register(_('work_is_done',
                 c('controllers.worker.work_is_done')))
    r.register(_('worker_connected',
                 c('controllers.worker.worker_connected')))
    r.register(_('worker_disconnected',
                 c('controllers.worker.worker_disconnected')))
    r.register(_('worker_requests_work',
                 c('controllers.worker.worker_requests_work')))


