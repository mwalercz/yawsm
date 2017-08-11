import datetime

from dq_broker.domain.worker.usecases.details import WorkerDetailsUsecase
from dq_broker.domain.worker.usecases.list import WorkerListUsecase
from dq_broker.domain.worker.usecases.worker_has_work import WorkerHasWorkUsecase
from dq_broker.domain.worker.usecases.work_is_done import WorkIsDoneUsecase
from dq_broker.domain.worker.usecases.worker_disconnected import WorkerDisconnectedUsecase
from dq_broker.domain.worker.usecases.worker_requests_work import WorkerRequestsWorkUsecase
from dq_broker.domain.worker.usecases.worker_system_stat import WorkerSystemStatUsecase
from dq_broker.domain.worker.usecases.worker_connected import WorkerConnectedUsecase


def work_is_done_usecase(c):
    return WorkIsDoneUsecase(
        workers_repo=c('worker_repo'),
        event_saver=c('event_saver')
    )


def worker_connected_usecase(c):
    return WorkerConnectedUsecase(
        workers_repo=c('worker_repo'),
        workers_notifier=c('workers_notifier')
    )


def worker_disconnected_usecase(c):
    return WorkerDisconnectedUsecase(
        workers_repo=c('worker_repo'),
        work_queue=c('work_queue'),
        event_saver=c('event_saver'),
        workers_notifier=c('workers_notifier'),
    )


def worker_requests_work_usecase(c):
    return WorkerRequestsWorkUsecase(
        work_queue=c('work_queue'),
        workers_repo=c('worker_repo'),
        worker_client=c('worker_client'),
        event_saver=c('event_saver')
    )


def worker_has_work_usecase(c):
    return WorkerHasWorkUsecase(
        workers_repo=c('worker_repo'),
        event_saver=c('event_saver')
    )


def worker_system_stat_usecase(c):
    return WorkerSystemStatUsecase(
        workers_repo=c('worker_repo'),
        current_datetime=datetime.datetime.now,
    )


def worker_list_usecase(c):
    return WorkerListUsecase(
        workers_repo=c('worker_repo')
    )


def worker_details_usecase(c):
    return WorkerDetailsUsecase(
        workers_repo=c('worker_repo')
    )


def register(c):
    c.add_service(work_is_done_usecase, 'usecases.worker.work_is_done')
    c.add_service(worker_connected_usecase, 'usecases.worker.worker_connected')
    c.add_service(worker_disconnected_usecase, 'usecases.worker.worker_disconnected')
    c.add_service(worker_requests_work_usecase, 'usecases.worker.worker_requests_work')
    c.add_service(worker_has_work_usecase, 'usecases.worker.worker_has_work')
    c.add_service(worker_system_stat_usecase, 'usecases.worker.system_stat')
    c.add_service(worker_list_usecase, 'usecases.worker.list')
    c.add_service(worker_details_usecase, 'usecases.worker.details')
