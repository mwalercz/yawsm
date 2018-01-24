from peewee import Model
from peewee_async import PostgresqlDatabase

database = PostgresqlDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database