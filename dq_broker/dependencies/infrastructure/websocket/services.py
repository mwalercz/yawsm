import ssl

import os

from definitions import ROOT_DIR
from dq_broker.infrastructure.websocket.factory import DqBrokerFactory
from dq_broker.infrastructure.websocket.protocol import DqBrokerProtocol
from dq_broker.infrastructure.websocket.routing import Router
from dq_broker.infrastructure.websocket.supervisor import Supervisor


def router(c):
    return Router()


def supervisor(c):
    return Supervisor(
        response_client=c('response_client'),
        router=c('router')
    )


def protocol(c):
    protocol = DqBrokerProtocol
    protocol.auth = c('worker_auth')
    protocol.deserializer = c('deserializer')
    protocol.supervisor = c('supervisor')
    return protocol


def factory(c):
    factory = DqBrokerFactory(
        url=c('conf')['websocket']['url'],
        loop=c('loop')
    )
    factory.protocol = c('protocol')
    factory.setProtocolOptions(
        autoPingInterval=c('conf').getfloat('websocket', 'auto_ping_interval'),
        autoPingTimeout=c('conf').getfloat('websocket', 'auto_ping_timeout')
    )
    return factory


def secure_context(c):
    secure_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # secure_context.verify_mode = ssl.CERT_REQUIRED
    secure_context.load_cert_chain(
        os.path.join(ROOT_DIR, c('conf')['auth']['crt_path']),
        os.path.join(ROOT_DIR, c('conf')['auth']['key_path']),
    )
    # secure_context.load_verify_locations(
    #     os.path.join(ROOT_DIR, 'keys/server.crt')
    # )
    return secure_context


def register(c):
    c.add_service(router)
    c.add_service(supervisor)
    c.add_service(protocol)
    c.add_service(factory)
    c.add_service(secure_context)
