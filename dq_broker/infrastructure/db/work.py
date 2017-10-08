import datetime

from peewee import CharField, PrimaryKeyField, TextField, DateTimeField, ForeignKeyField
from playhouse.sqlite_ext import JSONField

from dq_broker.infrastructure.db.base import BaseModel
from dq_broker.infrastructure.db.user import User
from dq_broker.work.model import ALL_WORK_STATUSES


class Work(BaseModel):
    class Meta:
        db_table = 'works'
        order_by = ('created_at', 'work_id')

    work_id = PrimaryKeyField()
    user = ForeignKeyField(User, index=True)
    command = CharField()
    cwd = CharField()
    env = JSONField(default={}, null=True)
    output = TextField(null=True)
    status = CharField(choices=ALL_WORK_STATUSES)
    created_at = DateTimeField(default=datetime.datetime.utcnow)


class WorkEvent(BaseModel):
    work = ForeignKeyField(Work, related_name='events')
    event_id = PrimaryKeyField()
    event_type = CharField()
    status = CharField(max_length=100, choices=ALL_WORK_STATUSES)
    context = JSONField(default={}, null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        db_table = 'work_events'
        order_by = ('created_at', 'event_id')
