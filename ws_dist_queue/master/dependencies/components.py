import asyncio

from peewee_async import Manager

from ws_dist_queue.lib.router import Router
from ws_dist_queue.master.components.authorization import Authorization, UserAuthorization, WorkerAuthorization
from ws_dist_queue.master.components.clients import UserClient, WorkerClient
from ws_dist_queue.master.components.factory import MasterFactory
from ws_dist_queue.master.components.protocol import MasterProtocol


def router(c):
    return Router()


def loop(c):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    return loop


def user_auth(c):
    return UserAuthorization()


def worker_auth(c):
    return WorkerAuthorization(c('conf')['worker']['api_key'])


def auth(c):
    auth = Authorization()
    auth.register(c('user_auth'))
    auth.register(c('worker_auth'))
    return auth


def protocol(c):
    protocol = MasterProtocol
    protocol.auth = c('auth')
    protocol.deserializer = c('deserializer')
    protocol.router = c('router')
    return protocol


def objects(c):
    objects = Manager(database=c('db'), loop=c('loop'))

    return objects


def factory(c):
    factory = MasterFactory(
        uri=c('conf')['master']['wss_uri']
    )
    factory.protocol = c('protocol')
    return factory


def user_client(c):
    return UserClient(c('serializer'))


def worker_client(c):
    return WorkerClient(c('serializer'))


def register(c):
    c.add_service(router)
    c.add_service(loop)
    c.add_service(user_auth)
    c.add_service(worker_auth)
    c.add_service(auth)
    c.add_service(objects)
    c.add_service(protocol)
    c.add_service(factory)
    c.add_service(user_client)
    c.add_service(worker_client)
