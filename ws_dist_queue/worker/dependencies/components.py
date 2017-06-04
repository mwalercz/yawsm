from ws_dist_queue.lib.router import Router
from ws_dist_queue.worker.components.authentication import Authentication
from ws_dist_queue.worker.components.factory import WorkerFactory
from ws_dist_queue.worker.components.master_client import MasterClient
from ws_dist_queue.worker.components.protocol import WorkerProtocol


def auth(c):
    return Authentication(c('conf')['worker']['api_key'])


def master_client(c):
    return MasterClient(
        serializer=c('serializer')
    )


def router(c):
    router = Router()
    router.register('worker', c('worker_controller'))
    return router


def protocol(c):
    protocol = WorkerProtocol
    protocol.serializer = c('serializer')
    protocol.deserializer = c('deserializer')
    protocol.master_client = c('master_client')
    protocol.router = c('router')
    return protocol


def factory(c):
    factory = WorkerFactory(
        wss_uri=c('conf')['master']['wss_uri'],
        headers=c('auth').get_headers()
    )
    factory.protocol = c('protocol')
    return factory


def register(c):
    c.add_service(auth)
    c.add_service(master_client)
    c.add_service(router)
    c.add_service(protocol)
    c.add_service(factory)
