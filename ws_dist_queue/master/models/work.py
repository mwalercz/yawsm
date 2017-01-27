from enum import Enum

from peewee import CharField, PrimaryKeyField, Model, TextField
from playhouse.postgres_ext import JSONField
from peewee_async import PostgresqlDatabase

database = PostgresqlDatabase(None)


class WorkStatus(Enum):
    received = 1
    processing = 2
    finished_with_success = 3
    finished_with_failure = 4
    work_killed = 5
    work_not_killed = 6
    worker_failure = 7

ALL_WORK_STATUSES = [e.name for e in WorkStatus]


class Work(Model):
    class Meta:
        db_table = 'works'
        database = database

    work_id = PrimaryKeyField()
    command = CharField()
    cwd = CharField()
    env = JSONField(default={}, null=True)
    status = CharField(choices=ALL_WORK_STATUSES)
    username = CharField()
    output = TextField(null=True)






