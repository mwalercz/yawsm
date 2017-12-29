def register_http_routing(r, c):
    r.add_route('GET', '/ping', c('controllers.ping').handle)

    r.add_route('GET', '/users/{username}/works', c('controllers.work.list').handle)
    r.add_route('GET', '/users/{username}/works/{work_id}', c('controllers.work.details').handle)
    r.add_route('POST', '/users/{username}/works', c('controllers.work.new').handle)
    r.add_route('DELETE', '/users/{username}/works/{work_id}', c('controllers.work.kill').handle)

    r.add_route('GET', '/workers', c('controllers.workers.list').handle)
    r.add_route('GET', '/workers/{worker_socket}', c('controllers.workers.details').handle)

    r.add_route('POST', '/users', c('controllers.user.new').handle)
