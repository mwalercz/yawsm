from yawsm.worker.actions.work_is_done.ws import WorkIsDoneController
from yawsm.worker.actions.worker_connected.ws import WorkerConnectedController
from yawsm.worker.actions.worker_disconnected.ws import WorkerDisconnectedController
from yawsm.worker.actions.worker_has_work.ws import WorkerHasWorkController
from yawsm.worker.actions.worker_requests_work.ws import WorkerRequestsWorkController
from yawsm.worker.actions.worker_system_stat.ws import WorkerSystemStatController


def work_is_done_controller(c):
    return WorkIsDoneController(
        usecase=c('actions.worker.work_is_done')
    )


def worker_connected_controller(c):
    return WorkerConnectedController(
        usecase=c('actions.worker.worker_connected')
    )


def worker_disconnected_controller(c):
    return WorkerDisconnectedController(
        usecase=c('actions.worker.worker_disconnected')
    )


def worker_requests_work_controller(c):
    return WorkerRequestsWorkController(
        usecase=c('actions.worker.worker_requests_work')
    )


def worker_has_work_controller(c):
    return WorkerHasWorkController(
        usecase=c('actions.worker.worker_has_work')
    )


def worker_system_stat_controller(c):
    return WorkerSystemStatController(
        usecase=c('actions.worker.system_stat')
    )


def register(c):
    c.add_service(work_is_done_controller, 'controllers.worker.work_is_done')
    c.add_service(worker_connected_controller, 'controllers.worker.worker_connected')
    c.add_service(worker_disconnected_controller, 'controllers.worker.worker_disconnected')
    c.add_service(worker_requests_work_controller, 'controllers.worker.worker_requests_work')
    c.add_service(worker_has_work_controller, 'controllers.worker.worker_has_work')
    c.add_service(worker_system_stat_controller, 'controllers.worker.system_stat')
