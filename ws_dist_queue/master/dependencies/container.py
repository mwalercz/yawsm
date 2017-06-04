import ssl
from configparser import ConfigParser

from ws_dist_queue.lib.serializers import JsonDeserializer, JsonSerializer
from ws_dist_queue.master.dependencies import components
from ws_dist_queue.master.dependencies import controllers
from ws_dist_queue.master.infrastructure.db.work import Work, database


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def db(c):
    database.init(**c('conf')['db'])
    Work.create_table(True)
    return database


def secure_context(c):
    secure_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    secure_context.load_cert_chain(
        c('conf')['auth']['crt_path'], c('conf')['auth']['key_path']
    )
    return secure_context


def deserializer(c):
    return JsonDeserializer()


def serializer(c):
    return JsonSerializer()


def register(c):
    c.add_service(conf)
    c.add_service(db)
    c.add_service(secure_context)
    c.add_service(deserializer)
    c.add_service(serializer)

    components.register(c)
    controllers.register(c)
