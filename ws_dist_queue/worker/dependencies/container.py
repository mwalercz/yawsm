import asyncio
from configparser import ConfigParser

from ws_dist_queue.lib.serializers import JsonDeserializer, JsonSerializer
from ws_dist_queue.worker.dependencies import components
from ws_dist_queue.worker.dependencies import controller


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def deserializer(c):
    return JsonDeserializer()


def serializer(c):
    return JsonSerializer()


def loop(c):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    return loop


def register(c):
    c.add_service(conf)
    c.add_service(deserializer)
    c.add_service(serializer)
    c.add_service(loop)

    components.register(c)
    controller.register(c)
