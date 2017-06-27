from ws_dist_queue.master.infrastructure.auth.base import Role


def register_routing(r, c):
    r.register('kill_work', c('controllers.user.kill_work'), Role.user)
    r.register('list_work', c('controllers.user.list_work'), Role.user)
    r.register('new_work', c('controllers.user.new_work'), Role.user)

    r.register('work_is_done',
               c('controllers.worker.work_is_done'),
               Role.worker)
    r.register('worker_connected',
               c('controllers.worker.worker_connected'),
               Role.worker)
    r.register('worker_disconnected',
               c('controllers.worker.worker_disconnected'),
               Role.worker)
    r.register('worker_requests_work',
               c('controllers.worker.worker_requests_work'),
               Role.worker)
