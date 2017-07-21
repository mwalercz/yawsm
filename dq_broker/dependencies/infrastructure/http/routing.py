

def register_http_routing(r, c):
    r.add_route('GET', '/ping', c('controllers.ping').handle)
    r.add_route('GET', '/users/{username}/works', c('controllers.work.list_work').handle)
    r.add_route('GET', '/users/{username}/works/{work_id}', c('controllers.work.work_details').handle)
    r.add_route('POST', '/users/{username}/works', c('controllers.work.new_work').handle)
    r.add_route('DELETE', '/users/{username}/works/{work_id}', c('controllers.work.kill_work').handle)
