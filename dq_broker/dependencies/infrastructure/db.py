from peewee_async import Manager

from dq_broker.infrastructure.db.base import database
from dq_broker.infrastructure.db.user import User
from dq_broker.infrastructure.db.work import Work, WorkEvent


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
    User.create_table(True)
    Work.create_table(True)
    WorkEvent.create_table(True)


def create_admin_if_does_not_exist():
    user, was_created = User.get_or_create(
        is_admin=True,
        defaults=dict(
            username='admin',
            password='admin',
            is_admin=True
        )
    )


def register(c):
    c.add_service(db)
    c.add_service(objects)
