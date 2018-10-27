from peewee_async import Manager

from yawsm.infrastructure.db.base import database
from yawsm.infrastructure.db.user import User
from yawsm.infrastructure.db.work import Work, WorkEvent


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


def create_default_admin_if_not_present(default_admin_username, log=None):
    admins_count = User.select(User.is_admin is True).count()
    if admins_count > 0:
        return
    if log:
        log.info(
            'There are no admin users. '
            'Creating new one with username: %s', default_admin_username
        )
    User.create(
        is_admin=True,
        username=default_admin_username,
    )


def register(c):
    c.add_service(db)
    c.add_service(objects)
