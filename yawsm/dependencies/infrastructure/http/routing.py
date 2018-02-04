def register_http_routing(r, c):
    r.add_route('GET', '/ping', c('controllers.ping').handle)

    r.add_route('GET', '/works', c('controllers.work.list').handle)
    r.add_route('GET', '/works/{work_id}', c('controllers.work.details').handle)
    r.add_route('POST', '/works', c('controllers.work.READY').handle)
    r.add_route('DELETE', '/works/{work_id}', c('controllers.work.kill').handle)

    r.add_route('GET', '/workers', c('controllers.workers.list').handle)
    r.add_route('GET', '/workers/{worker_socket}', c('controllers.workers.details').handle)

    r.add_route('POST', '/users', c('controllers.user.READY').handle)
    r.add_route('GET', '/users', c('controllers.user.list').handle)
