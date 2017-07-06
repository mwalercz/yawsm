import asyncio

from ws_dist_queue.master.infrastructure.loop_policy import StrictEventLoopPolicy
from ws_dist_queue.master.infrastructure.services.routing import Router
from ws_dist_queue.master.infrastructure.services.supervisor import Supervisor

from ws_dist_queue.lib.serializers import JsonDeserializer, JsonSerializer
from ws_dist_queue.master.infrastructure.services.executor import Executor


def router(c):
    return Router(auth=c('auth'))


def supervisor(c):
    return Supervisor(
        executor=Executor(),
        response_client=c('response_client'),
        router=c('router')
    )


def deserializer(c):
    return JsonDeserializer()


def serializer(c):
    return JsonSerializer()


def register(c):
    c.add_service(router)
    c.add_service(supervisor)
    c.add_service(deserializer)
    c.add_service(serializer)
