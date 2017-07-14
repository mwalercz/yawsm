import ssl

from infrastructure.websocket.factory import DqBrokerFactory
from infrastructure.websocket.protocol import DqBrokerProtocol
from infrastructure.websocket.routing import Router
from infrastructure.websocket.supervisor import Supervisor


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
        url=c('conf')['websocket']['url']
    )
    factory.protocol = c('protocol')
    factory.setProtocolOptions(
        autoPingInterval=c('conf').getint('websocket', 'auto_ping_interval'),
        autoPingTimeout=c('conf').getint('websocket', 'auto_ping_timeout')
    )
    return factory


def secure_context(c):
    secure_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    secure_context.load_cert_chain(
        c('conf')['auth']['crt_path'], c('conf')['auth']['key_path']
    )
    return secure_context


def register(c):
    c.add_service(router)
    c.add_service(supervisor)
    c.add_service(protocol)
    c.add_service(factory)
    c.add_service(secure_context)
