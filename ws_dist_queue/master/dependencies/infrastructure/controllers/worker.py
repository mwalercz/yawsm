from ws_dist_queue.master.infrastructure.controllers.worker.work_is_done import WorkIsDoneController
from ws_dist_queue.master.infrastructure.controllers.worker.worker_connected import WorkerConnectedController
from ws_dist_queue.master.infrastructure.controllers.worker.worker_disconnected import WorkerDisconnectedController
from ws_dist_queue.master.infrastructure.controllers.worker.worker_requests_work import WorkerRequestsWorkController


def work_is_done_controller(c):
    return WorkIsDoneController(
        usecase=c('usecases.worker.work_is_done')
    )


def worker_connected_controller(c):
    return WorkerConnectedController(
        usecase=c('usecases.worker.worker_connected')
    )


def worker_disconnected_controller(c):
    return WorkerDisconnectedController(
        usecase=c('usecases.worker.worker_disconnected')
    )


def worker_requests_work_controller(c):
    return WorkerRequestsWorkController(
        usecase=c('usecases.worker.worker_requests_work')
    )


def register(c):
    c.add_service(work_is_done_controller, 'controllers.worker.work_is_done')
    c.add_service(worker_connected_controller, 'controllers.worker.worker_connected')
    c.add_service(worker_disconnected_controller, 'controllers.worker.worker_disconnected')
    c.add_service(worker_requests_work_controller, 'controllers.worker.worker_requests_work')