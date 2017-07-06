import datetime

from peewee import CharField, PrimaryKeyField, Model, TextField, DateTimeField, ForeignKeyField
from peewee_async import PostgresqlDatabase
from playhouse.sqlite_ext import JSONField

from dq_broker.domain.work.model import ALL_WORK_STATUSES

database = PostgresqlDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class Work(BaseModel):
    class Meta:
        db_table = 'works'
        order_by = ('created_at', 'work_id')

    work_id = PrimaryKeyField()
    command = CharField()
    cwd = CharField()
    env = JSONField(default={}, null=True)
    username = CharField()
    output = TextField(null=True)
    status = CharField(choices=ALL_WORK_STATUSES)
    created_at = DateTimeField(default=datetime.datetime.utcnow)


class WorkEvent(BaseModel):
    work_id = ForeignKeyField(Work, related_name='events')
    event_id = PrimaryKeyField()
    event_type = CharField()
    status = CharField(choices=ALL_WORK_STATUSES)
    context = JSONField(default={}, null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        db_table = 'work_events'
        order_by = ('created_at', 'event_id')

