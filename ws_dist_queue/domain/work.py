from peewee import Model, CharField, PostgresqlDatabase
import ws_dist_queue.settings.defaults as conf


class Work(Model):
    command = CharField()
    cwd = CharField()
    username = CharField()
    password = CharField()

    class Meta:
        database=PostgresqlDatabase(**conf.DB_CONF)
