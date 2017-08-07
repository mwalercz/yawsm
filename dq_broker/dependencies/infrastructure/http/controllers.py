from dq_broker.infrastructure.http.controllers.work.kill import KillWorkController
from dq_broker.infrastructure.http.controllers.work.list import ListWorksController
from dq_broker.infrastructure.http.controllers.work.new import NewWorkController
from dq_broker.infrastructure.http.controllers.work.details import WorkDetailsController
from dq_broker.infrastructure.http.controllers.ping import PingController
from dq_broker.infrastructure.http.controllers.worker.details import WorkerDetailsController
from dq_broker.infrastructure.http.controllers.worker.list import WorkerListController


def ping_controller(c):
    return PingController()


def kill_work_controller(c):
    return KillWorkController(
        usecase=c('usecases.work.kill_work'),
    )


def work_list_controller(c):
    return ListWorksController(
        usecase=c('usecases.work.list_work'),
    )


def new_work_controller(c):
    return NewWorkController(
        usecase=c('usecases.work.new_work'),
    )


def work_details_controller(c):
    return WorkDetailsController(
        usecase=c('usecases.work.work_details'),
    )


def worker_list_controller(c):
    return WorkerListController(
        usecase=c('usecases.worker.list')
    )


def worker_details_controller(c):
    return WorkerDetailsController(
        usecase=c('usecases.worker.details')
    )


def register(c):
    c.add_service(ping_controller, 'controllers.ping')
    c.add_service(kill_work_controller, 'controllers.work.kill')
    c.add_service(new_work_controller, 'controllers.work.new')
    c.add_service(work_details_controller, 'controllers.work.details')
    c.add_service(work_list_controller, 'controllers.work.list')

    c.add_service(worker_details_controller, 'controllers.worker.details')
    c.add_service(worker_details_controller, 'controllers.worker.list')

