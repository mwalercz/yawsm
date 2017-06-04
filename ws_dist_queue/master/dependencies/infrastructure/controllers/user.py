from ws_dist_queue.master.infrastructure.controllers.user.kill_work import KillWorkController
from ws_dist_queue.master.infrastructure.controllers.user.list_work import ListWorkController
from ws_dist_queue.master.infrastructure.controllers.user.new_work import NewWorkController


def kill_work_controller(c):
    return KillWorkController(
        user_auth=c('auth.user'),
        usecase=c('usecases.user.kill_work'),
        user_client=c('clients.user'),
    )


def list_work_controller(c):
    return ListWorkController(
        user_auth=c('auth.user'),
        usecase=c('usecases.user.list_work'),
        user_client=c('clients.user')
    )


def new_work_controller(c):
    return NewWorkController(
        user_auth=c('auth.user'),
        usecase=c('usecases.user.new_work'),
        user_client=c('clients.user'),
    )


def register(c):
    c.add_service(kill_work_controller, 'controllers.user.kill_work')
    c.add_service(list_work_controller, 'controllers.user.list_work')
    c.add_service(new_work_controller, 'controllers.user.new_work')