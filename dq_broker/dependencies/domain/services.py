from dq_broker.domain.work.work_queue import WorkQueue
from dq_broker.domain.worker.notifier import WorkersNotifier
from dq_broker.domain.worker.picker import FreeWorkersPicker
from dq_broker.domain.worker.repository import WorkersRepository
from dq_broker.infrastructure.repositories.user import UserRepository
from dq_broker.infrastructure.repositories.work import WorkEventSaver, WorkSaver, WorkFinder
from dq_broker.infrastructure.repositories.worker import InMemoryWorkers


def picker(c):
    return FreeWorkersPicker()


def workers_notifier(c):
    return WorkersNotifier(
        work_queue=c('work_queue'),
        picker=c('picker'),
        workers=c('workers'),
        worker_client=c('worker_client'),
    )


def work_queue(c):
    return WorkQueue()


def user_repo(c):
    return UserRepository(
        objects=c('objects')
    )


def workers(c):
    return InMemoryWorkers()


def workers_repo(c):
    return WorkersRepository(
        objects=c('objects')
    )


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

    c.add_service(user_repo)
    c.add_service(work_queue)
    c.add_service(workers)

    c.add_service(event_saver)
    c.add_service(work_saver)
    c.add_service(work_finder)
    c.add_service(workers_repo)
