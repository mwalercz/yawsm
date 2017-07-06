from dq_broker.infrastructure.controllers.user.kill_work import KillWorkController
from dq_broker.infrastructure.controllers.user.list_work import ListWorkController
from dq_broker.infrastructure.controllers.user.work_details import WorkDetailsController

from dq_broker.infrastructure.controllers.user.new_work import NewWorkController


def kill_work_controller(c):
    return KillWorkController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.kill_work'),
    )


def list_work_controller(c):
    return ListWorkController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.list_work'),
    )


def new_work_controller(c):
    return NewWorkController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.new_work'),
    )


def work_details_controller(c):
    return WorkDetailsController(
        user_auth=c('user_auth'),
        usecase=c('usecases.user.work_details'),
    )


def register(c):
    c.add_service(kill_work_controller, 'controllers.user.kill_work')
    c.add_service(list_work_controller, 'controllers.user.list_work')
    c.add_service(new_work_controller, 'controllers.user.new_work')
    c.add_service(work_details_controller, 'controllers.user.work_details')
