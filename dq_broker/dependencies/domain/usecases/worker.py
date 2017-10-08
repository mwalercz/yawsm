import datetime

from dq_broker.worker.actions.details.usecase import WorkerDetailsUsecase
from dq_broker.worker.actions.list.usecase import WorkerListUsecase
from dq_broker.worker.actions.work_is_done.usecase import WorkIsDoneUsecase
from dq_broker.worker.actions.worker_connected.usecase import WorkerConnectedUsecase
from dq_broker.worker.actions.worker_disconnected.usecase import WorkerDisconnectedUsecase
from dq_broker.worker.actions.worker_has_work.usecase import WorkerHasWorkUsecase
from dq_broker.worker.actions.worker_requests_work.usecase import WorkerRequestsWorkUsecase
from dq_broker.worker.actions.worker_system_stat.usecase import WorkerSystemStatUsecase


def work_is_done_usecase(c):
    return WorkIsDoneUsecase(
        workers=c('workers'),
        event_saver=c('event_saver')
    )


def worker_connected_usecase(c):
    return WorkerConnectedUsecase(
        workers=c('workers'),
        workers_notifier=c('workers_notifier'),
        hosts=c('hosts')
    )


def worker_disconnected_usecase(c):
    return WorkerDisconnectedUsecase(
        workers=c('workers'),
        work_queue=c('work_queue'),
        event_saver=c('event_saver'),
        workers_notifier=c('workers_notifier'),
    )


def worker_requests_work_usecase(c):
    return WorkerRequestsWorkUsecase(
        work_queue=c('work_queue'),
        workers=c('workers'),
        worker_client=c('worker_client'),
        event_saver=c('event_saver'),
        notifier=c('workers_notifier')
    )


def worker_has_work_usecase(c):
    return WorkerHasWorkUsecase(
        workers=c('workers'),
        event_saver=c('event_saver')
    )


def worker_system_stat_usecase(c):
    return WorkerSystemStatUsecase(
        workers=c('workers'),
        current_datetime=datetime.datetime.now,
    )


def worker_list_usecase(c):
    return WorkerListUsecase(
        workers=c('workers')
    )


def worker_details_usecase(c):
    return WorkerDetailsUsecase(
        workers=c('workers')
    )


def register(c):
    c.add_service(work_is_done_usecase, 'actions.worker.work_is_done')
    c.add_service(worker_connected_usecase, 'actions.worker.worker_connected')
    c.add_service(worker_disconnected_usecase, 'actions.worker.worker_disconnected')
    c.add_service(worker_requests_work_usecase, 'actions.worker.worker_requests_work')
    c.add_service(worker_has_work_usecase, 'actions.worker.worker_has_work')
    c.add_service(worker_system_stat_usecase, 'actions.worker.system_stat')
    c.add_service(worker_list_usecase, 'actions.worker.list')
    c.add_service(worker_details_usecase, 'actions.worker.details')
