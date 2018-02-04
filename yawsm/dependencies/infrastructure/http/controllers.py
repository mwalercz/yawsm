from yawsm.infrastructure.http.controllers.ping import PingController
from yawsm.user.actions.list.http import ListUserController
from yawsm.user.actions.new.http import NewUserController
from yawsm.work.actions.details.http import WorkDetailsController
from yawsm.work.actions.kill.http import KillWorkController
from yawsm.work.actions.list.http import ListWorksController
from yawsm.work.actions.new.http import NewWorkController
from yawsm.worker.actions.details.http import WorkerDetailsController
from yawsm.worker.actions.list.http import WorkerListController


def ping_controller(c):
    return PingController()


def kill_work_controller(c):
    return KillWorkController(
        usecase=c('actions.work.kill_work'),
    )


def work_list_controller(c):
    return ListWorksController(
        usecase=c('actions.work.list_work'),
    )


def new_work_controller(c):
    return NewWorkController(
        usecase=c('actions.work.new_work'),
    )


def work_details_controller(c):
    return WorkDetailsController(
        usecase=c('actions.work.work_details'),
    )


def worker_list_controller(c):
    return WorkerListController(
        usecase=c('actions.worker.list')
    )


def worker_details_controller(c):
    return WorkerDetailsController(
        usecase=c('actions.worker.details')
    )


def new_user_controller(c):
    return NewUserController(
        usecase=c('actions.user.new')
    )


def list_user_controller(c):
    return ListUserController(
        usecase=c('actions.user.list')
    )


def register(c):
    c.add_service(ping_controller, 'controllers.ping')
    c.add_service(kill_work_controller, 'controllers.work.kill')
    c.add_service(new_work_controller, 'controllers.work.READY')
    c.add_service(work_details_controller, 'controllers.work.details')
    c.add_service(work_list_controller, 'controllers.work.list')

    c.add_service(worker_details_controller, 'controllers.workers.details')
    c.add_service(worker_list_controller, 'controllers.workers.list')

    c.add_service(new_user_controller, 'controllers.user.READY')
    c.add_service(list_user_controller, 'controllers.user.list')
