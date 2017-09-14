from peewee import PrimaryKeyField, FloatField, ForeignKeyField, CharField, DateTimeField

from dq_broker.infrastructure.db.base import BaseModel


class Host(BaseModel):
    host_id = PrimaryKeyField()
    host_address = CharField(unique=True)


class SystemStat(BaseModel):
    stat_id = PrimaryKeyField()
    load_1 = FloatField()
    load_5 = FloatField()
    load_15 = FloatField()
    created_at = DateTimeField()
    host = ForeignKeyField(Host, related_name='stats')


class Worker(BaseModel):
    worker_id = PrimaryKeyField()
    worker_socket = CharField()
    host = ForeignKeyField(Host, related_name='workers')
