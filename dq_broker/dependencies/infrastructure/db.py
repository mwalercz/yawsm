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
    Work.create_table(True)
    WorkEvent.create_table(True)
    return database


def objects(c):
    return Manager(database=c('db'), loop=c('loop'))


def register(c):
    c.add_service(db)
    c.add_service(objects)
