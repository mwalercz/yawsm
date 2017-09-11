from peewee import PrimaryKeyField, FloatField, ForeignKeyField, CharField

from dq_broker.infrastructure.db.base import BaseModel


class Host(BaseModel):
    host_id = PrimaryKeyField()
    host_address = CharField(unique=True)


class SystemStat(BaseModel):
    stat_id = PrimaryKeyField()
    load = FloatField()
    host = ForeignKeyField(Host, related_name='stats')


class Worker(BaseModel):
    worker_id = PrimaryKeyField()
    worker_socket = CharField()
    host = ForeignKeyField(Host, related_name='workers')
