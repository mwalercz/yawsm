

def register_http_routing(r, c):
    r.add_route('GET', '/works', c('controllers.work.list_work').handle)
    r.add_route('GET', '/works/{work_id}', c('controllers.work.work_details').handle)
    r.add_route('POST', '/works', c('controllers.work.new_work').handle)
    r.add_route('DELETE', '/works/{work_id}', c('controllers.work.kill_work').handle)
