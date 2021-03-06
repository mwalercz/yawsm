import asyncio

from yawsm.work.actions.consumer import NewWorkConsumer
from yawsm.worker.hosts import InMemoryHosts
from yawsm.worker.notifier import WorkersNotifier

from yawsm.infrastructure.repositories.user import UserRepository
from yawsm.infrastructure.repositories.work import WorkEventSaver, WorkSaver, WorkFinder
from yawsm.infrastructure.repositories.worker import InMemoryWorkers
from yawsm.work.work_queue import WorkQueue
from yawsm.worker.picker import SystemInfoBasedPicker


def picker(c):
    return SystemInfoBasedPicker(delay=0)
    # return FreeWorkersPicker()


def workers_notifier(c):
    return WorkersNotifier(
        work_queue=c('work_queue'),
        picker=c('picker'),
        workers=c('workers'),
        worker_client=c('worker_client'),
    )


def task_queue(c):
    return asyncio.Queue(loop=c('loop'))


def work_queue(c):
    return WorkQueue()


def user_repo(c):
    return UserRepository(
        objects=c('objects')
    )


def workers(c):
    return InMemoryWorkers()


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


def hosts(c):
    return InMemoryHosts()


def consumer(c):
    return NewWorkConsumer(
        workers_notifier=c('workers_notifier'),
        queue=c('task_queue'),
    )


def register(c):
    c.add_service(picker)
    c.add_service(workers_notifier)
    c.add_service(task_queue)

    c.add_service(user_repo)
    c.add_service(work_queue)
    c.add_service(workers)

    c.add_service(event_saver)
    c.add_service(work_saver)
    c.add_service(work_finder)
    c.add_service(hosts)

    c.add_service(consumer)
