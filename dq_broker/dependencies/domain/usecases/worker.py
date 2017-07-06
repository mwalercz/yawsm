from dq_broker.domain.workers.usecases.work_is_done import WorkIsDoneUsecase
from dq_broker.domain.workers.usecases.worker_disconnected import WorkerDisconnectedUsecase
from dq_broker.domain.workers.usecases.worker_requests_work import WorkerRequestsWorkUsecase

from dq_broker.domain.workers.usecases.worker_connected import WorkerConnectedUsecase


def work_is_done_usecase(c):
    return WorkIsDoneUsecase(
        workers_repo=c('workers_repo'),
        event_saver=c('event_saver')
    )


def worker_connected_usecase(c):
    return WorkerConnectedUsecase(
        workers_repo=c('workers_repo'),
        workers_notifier=c('workers_notifier')
    )


def worker_disconnected_usecase(c):
    return WorkerDisconnectedUsecase(
        workers_repo=c('workers_repo'),
        work_queue=c('work_queue'),
        event_saver=c('event_saver'),
        workers_notifier=c('workers_notifier'),
    )


def worker_requests_work_usecase(c):
    return WorkerRequestsWorkUsecase(
        work_queue=c('work_queue'),
        workers_repo=c('workers_repo'),
        worker_client=c('worker_client'),
        event_saver=c('event_saver')
    )


def register(c):
    c.add_service(work_is_done_usecase, 'usecases.worker.work_is_done')
    c.add_service(worker_connected_usecase, 'usecases.worker.worker_connected')
    c.add_service(worker_disconnected_usecase, 'usecases.worker.worker_disconnected')
    c.add_service(worker_requests_work_usecase, 'usecases.worker.worker_requests_work')

