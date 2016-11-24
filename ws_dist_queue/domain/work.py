from peewee import Model, CharField, PostgresqlDatabase, IntegerField, PrimaryKeyField
import ws_dist_queue.settings.defaults as conf
from playhouse.postgres_ext import JSONField
from ws_dist_queue.model.work import ALL_WORK_STATUSES


class Work(Model):
    work_id = PrimaryKeyField()
    command = CharField()
    cwd = CharField()
    env = JSONField(default={}, null=True)
    status = CharField(choices=ALL_WORK_STATUSES)
    username = CharField(index=True)
    password = CharField()

    class Meta:
        database = PostgresqlDatabase(**conf.DB_CONF)
