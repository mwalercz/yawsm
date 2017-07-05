from ws_dist_queue.master.infrastructure.auth.base import ALL_ROLES, USER_ROLES, WORKER_ROLES
from ws_dist_queue.master.infrastructure.services.routing import Route as _


def register_routing(r, c):
    r.register_default(_('default',
                         c('controllers.default'),
                         ALL_ROLES))

    r.register(_('kill_work', c('controllers.user.kill_work'), USER_ROLES))
    r.register(_('list_work', c('controllers.user.list_work'), USER_ROLES))
    r.register(_('new_work', c('controllers.user.new_work'), USER_ROLES))

    r.register(_('work_is_done',
                 c('controllers.worker.work_is_done'),
                 WORKER_ROLES))
    r.register(_('worker_connected',
                 c('controllers.worker.worker_connected'),
                 WORKER_ROLES))
    r.register(_('worker_disconnected',
                 c('controllers.worker.worker_disconnected'),
                 WORKER_ROLES))
    r.register(_('worker_requests_work',
                 c('controllers.worker.worker_requests_work'),
                 WORKER_ROLES))


