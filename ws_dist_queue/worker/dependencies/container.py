import asyncio
import ssl
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

from ws_dist_queue.lib.serializers import JsonDeserializer, JsonSerializer
from ws_dist_queue.worker.dependencies import components
from ws_dist_queue.worker.dependencies import controller
from ws_dist_queue.worker.worker_app import WorkerApp


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def deserializer(c):
    return JsonDeserializer()


def serializer(c):
    return JsonSerializer()


def thread_pool_executor(c):
    return ThreadPoolExecutor(max_workers=2)


def loop(c):
    loop = asyncio.get_event_loop()
    loop.set_default_executor(c('thread_pool_executor'))
    loop.set_debug(True)
    return loop


def ssl_context(c):
    return ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23)


def app(c):
    return WorkerApp(
        host=c('conf')['master']['host'],
        port=c('conf')['master']['port'],
        factory=c('factory'),
        loop=c('loop'),
        controller=c('worker_controller'),
    )


def register(c):
    c.add_service(conf)
    c.add_service(deserializer)
    c.add_service(serializer)
    c.add_service(thread_pool_executor)
    c.add_service(loop)
    c.add_service(ssl_context)
    c.add_service(app)

    components.register(c)
    controller.register(c)
