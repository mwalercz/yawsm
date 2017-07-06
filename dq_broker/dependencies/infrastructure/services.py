from dq_broker.infrastructure.services.executor import Executor
from dq_broker.infrastructure.services.routing import Router
from dq_broker.infrastructure.services.supervisor import Supervisor

from dq_broker.lib.serializers import JsonDeserializer, JsonSerializer


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
