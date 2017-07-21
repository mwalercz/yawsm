from dq_broker.infrastructure.http.controllers.user.kill_work import KillWorkController
from dq_broker.infrastructure.http.controllers.user.list_work import ListWorkController
from dq_broker.infrastructure.http.controllers.user.new_work import NewWorkController
from dq_broker.infrastructure.http.controllers.user.work_details import WorkDetailsController
from dq_broker.infrastructure.http.controllers.ping import PingController


def ping_controller(c):
    return PingController()


def kill_work_controller(c):
    return KillWorkController(
        usecase=c('usecases.user.kill_work'),
    )


def list_work_controller(c):
    return ListWorkController(
        usecase=c('usecases.user.list_work'),
    )


def new_work_controller(c):
    return NewWorkController(
        usecase=c('usecases.user.new_work'),
    )


def work_details_controller(c):
    return WorkDetailsController(
        usecase=c('usecases.user.work_details'),
    )


def register(c):
    c.add_service(ping_controller, 'controllers.ping')
    c.add_service(kill_work_controller, 'controllers.work.kill_work')
    c.add_service(list_work_controller, 'controllers.work.list_work')
    c.add_service(new_work_controller, 'controllers.work.new_work')
    c.add_service(work_details_controller, 'controllers.work.work_details')
