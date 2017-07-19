from dq_broker.infrastructure.websocket.controllers.worker.worker_connected import WorkerConnectedController
from dq_broker.infrastructure.websocket.controllers.worker.worker_disconnected import WorkerDisconnectedController
from dq_broker.infrastructure.websocket.controllers.worker.worker_requests_work import WorkerRequestsWorkController

from dq_broker.infrastructure.websocket.controllers.worker.work_is_done import WorkIsDoneController
from dq_broker.infrastructure.websocket.controllers.worker.worker_has_work import WorkerHasWorkController


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


def worker_has_work_controller(c):
    return WorkerHasWorkController(
        usecase=c('usecases.worker.worker_has_work')
    )


def register(c):
    c.add_service(work_is_done_controller, 'controllers.worker.work_is_done')
    c.add_service(worker_connected_controller, 'controllers.worker.worker_connected')
    c.add_service(worker_disconnected_controller, 'controllers.worker.worker_disconnected')
    c.add_service(worker_requests_work_controller, 'controllers.worker.worker_requests_work')
    c.add_service(worker_has_work_controller, 'controllers.worker.worker_has_work')

