from ws_dist_queue.master.infrastructure.controllers.user.kill_work import KillWorkController
from ws_dist_queue.master.infrastructure.controllers.user.list_work import ListWorkController
from ws_dist_queue.master.infrastructure.controllers.user.new_work import NewWorkController
from ws_dist_queue.master.infrastructure.controllers.user.work_details import WorkDetailsController


def kill_work_controller(c):
    return KillWorkController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.kill_work'),
        user_client=c('user_client'),
    )


def list_work_controller(c):
    return ListWorkController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.list_work'),
        user_client=c('user_client')
    )


def new_work_controller(c):
    return NewWorkController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.new_work'),
        user_client=c('user_client'),
    )


def work_details_controller(c):
    return WorkDetailsController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.work_details'),
        user_client=c('user_client'),
    )


def register(c):
    c.add_service(kill_work_controller, 'controllers.user.kill_work')
    c.add_service(list_work_controller, 'controllers.user.list_work')
    c.add_service(new_work_controller, 'controllers.user.new_work')
    c.add_service(work_details_controller, 'controllers.user.work_details')
