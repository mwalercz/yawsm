import datetime
from peewee import CharField, PrimaryKeyField, Model, TextField, DateTimeField, ForeignKeyField, UUIDField
from playhouse.postgres_ext import JSONField
from peewee_async import PostgresqlDatabase

from ws_dist_queue.master.domain.work.model import ALL_WORK_STATUSES

database = PostgresqlDatabase(None, autocommit=False, autorollback=True)


class Work(Model):
    class Meta:
        db_table = 'works'
        database = database

    work_id = UUIDField(primary_key=True)
    command = CharField()
    cwd = CharField()
    env = JSONField(default={}, null=True)
    username = CharField()
    output = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)


class WorkEvent(Model):
    class Meta:
        db_table = 'work_events'
        database = database

    work_id = ForeignKeyField(Work)
    event_id = PrimaryKeyField()
    event_type = CharField()
    status = CharField(choices=ALL_WORK_STATUSES)
    context = JSONField(default={}, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)