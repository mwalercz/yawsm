import datetime

from peewee import CharField, PrimaryKeyField, TextField, DateTimeField, ForeignKeyField, IntegerField
from playhouse.sqlite_ext import JSONField

from yawsm.infrastructure.db.base import BaseModel
from yawsm.infrastructure.db.user import User
from yawsm.work.model import ALL_STATUSES


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
    exit_code = IntegerField(null=True)
    status = CharField(choices=ALL_STATUSES)
    created_at = DateTimeField(default=datetime.datetime.utcnow)


class WorkEvent(BaseModel):
    work = ForeignKeyField(Work, related_name='events')
    event_id = PrimaryKeyField()
    event_type = CharField()
    status = CharField(max_length=100, choices=ALL_STATUSES)
    context = JSONField(default={}, null=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        db_table = 'work_events'
        order_by = ('created_at', 'event_id')
