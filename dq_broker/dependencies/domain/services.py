from dq_broker.domain.work.repository import WorkEventSaver, WorkSaver, WorkFinder
from dq_broker.domain.workers.notifier import WorkersNotifier
from dq_broker.domain.workers.picker import FreeWorkersPicker
from dq_broker.domain.workers.repository import WorkersRepository

from dq_broker.domain.work.work_queue import WorkQueue


def picker(c):
    return FreeWorkersPicker()


def workers_notifier(c):
    return WorkersNotifier(
        work_queue=c('work_queue'),
        picker=c('picker'),
        workers_repo=c('workers_repo'),
        worker_client=c('worker_client'),
    )


def work_queue(c):
    return WorkQueue()


def workers_repo(c):
    return WorkersRepository()


def event_saver(c):
    return WorkEventSaver(
        objects=c('objects')
    )


def work_saver(c):
    return WorkSaver(
        objects=c('objects')
    )


def work_finder(c):
    return WorkFinder(
        objects=c('objects')
    )


def register(c):
    c.add_service(picker)
    c.add_service(workers_notifier)

    c.add_service(work_queue)
    c.add_service(workers_repo)

    c.add_service(event_saver)
    c.add_service(work_saver)
    c.add_service(work_finder)

