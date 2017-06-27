import asyncio

from ws_dist_queue.lib.serializers import JsonDeserializer, JsonSerializer
from ws_dist_queue.master.infrastructure.auth.base import AuthenticationService
from ws_dist_queue.master.infrastructure.auth.user import UserAuthenticationService
from ws_dist_queue.master.infrastructure.auth.worker import WorkerAuthenticationService
from ws_dist_queue.master.infrastructure.task_scheduler import TaskScheduler


def loop(c):
    loop = asyncio.get_event_loop()
    return loop


def user_auth(c):
    return UserAuthenticationService()


def worker_auth(c):
    return WorkerAuthenticationService(c('conf')['worker']['api_key'])


def auth(c):
    auth = AuthenticationService()
    auth.register(c('user_auth'))
    auth.register(c('worker_auth'))
    return auth


def task_scheduler(c):
    return TaskScheduler()


def deserializer(c):
    return JsonDeserializer()


def serializer(c):
    return JsonSerializer()


def register(c):
    c.add_service(loop)
    c.add_service(user_auth)
    c.add_service(worker_auth)
    c.add_service(auth)
    c.add_service(task_scheduler)
    c.add_service(deserializer)
    c.add_service(serializer)
