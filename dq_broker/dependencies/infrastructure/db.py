from peewee_async import Manager

from dq_broker.infrastructure.db.work import database, Work, WorkEvent


def db(c):
    db_conf = c('conf')['db']
    database.init(
        database=db_conf['database'],
        user=db_conf['user'],
        password=db_conf['password'],
        host=db_conf['host']
    )
    return database


def objects(c):
    return Manager(database=c('db'), loop=c('loop'))


def connect_to_db_and_create_tables():
    database.connect()
    Work.create_table(True)
    WorkEvent.create_table(True)


def register(c):
    c.add_service(db)
    c.add_service(objects)
