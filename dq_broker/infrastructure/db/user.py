from peewee import PrimaryKeyField, CharField, BooleanField

from dq_broker.infrastructure.db.base import BaseModel


class User(BaseModel):
    user_id = PrimaryKeyField()
    username = CharField(max_length=30, index=True, unique=True)
    is_admin = BooleanField()

    class Meta:
        db_table = 'users'
