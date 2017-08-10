from peewee_async import Manager

from dq_broker.domain.exceptions import UserNotFound
from dq_broker.infrastructure.db.user import User


class UserRepository:
    def __init__(self, objects: Manager):
        self.objects = objects

    async def find_by_username(self, username):
        query = User.select().where(
            User.username == username
        ).limit(1)
        result = await self.objects.execute(query)
        try:
            return list(result)[0]
        except IndexError:
            raise UserNotFound(username=username)

    async def get_or_create(self, username) -> User:
        return self.objects.get_or_create(
            User,
            defaults={
                'username': username,
                'is_admin': False,
            },
            username=username,
        )
