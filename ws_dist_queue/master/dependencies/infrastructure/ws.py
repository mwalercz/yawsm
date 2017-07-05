import ssl

from ws_dist_queue.master.infrastructure.ws.factory import MasterFactory
from ws_dist_queue.master.infrastructure.ws.protocol import MasterProtocol


def protocol(c):
    protocol = MasterProtocol
    protocol.auth = c('auth')
    protocol.deserializer = c('deserializer')
    protocol.supervisor = c('supervisor')
    return protocol


def factory(c):
    factory = MasterFactory(
        uri=c('conf')['master']['wss_uri']
    )
    factory.protocol = c('protocol')
    factory.setProtocolOptions(
        autoPingInterval=c('conf')['websocket']['auto_ping_interval'],
        autoPingTimeout=c('conf')['websocket']['auto_ping_timeout']
    )
    return factory


def secure_context(c):
    secure_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    secure_context.load_cert_chain(
        c('conf')['auth']['crt_path'], c('conf')['auth']['key_path']
    )
    return secure_context


def register(c):
    c.add_service(protocol)
    c.add_service(factory)
    c.add_service(secure_context)
