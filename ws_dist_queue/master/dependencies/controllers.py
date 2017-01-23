from collections import deque

from ws_dist_queue.master.controllers.base import WorkerPicker
from ws_dist_queue.master.controllers.user import UserController
from ws_dist_queue.master.controllers.worker import WorkerController


def work_queue(c):
    return deque()


def workers(c):
    return {}


def picker(c):
    return WorkerPicker()


def worker_controller(c):
    return WorkerController(
        work_queue=c('work_queue'),
        workers=c('workers'),
        picker=c('picker'),
        worker_client=c('worker_client'),
        user_client=c('user_client'),
        objects=c('objects'),
    )


def user_controller(c):
    return UserController(
        work_queue=c('work_queue'),
        workers=c('workers'),
        picker=c('picker'),
        worker_client=c('worker_client'),
        user_client=c('user_client'),
        user_auth=c('user_auth'),
        objects=c('objects'),
    )


def register(c):
    c.add_service(work_queue)
    c.add_service(workers)
    c.add_service(picker)
    c.add_service(worker_controller)
    c.add_service(user_controller)