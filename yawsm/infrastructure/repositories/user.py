from peewee import IntegrityError
from peewee_async import Manager

from yawsm.exceptions import UserNotFound
from yawsm.infrastructure.db.user import User


class UserAlreadyExists(Exception):
    def __init__(self, username):
        self.username = username


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

    async def create(self, user_dto) -> User:
        try:
            return await self.objects.create(
                User,
                username=user_dto.username,
                is_admin=user_dto.is_admin,
            )
        except IntegrityError:
            raise UserAlreadyExists(user_dto.username)

    async def get_or_create(self, username) -> User:
        return await self.objects.get_or_create(
            User,
            defaults={
                'username': username,
                'is_admin': False,
            },
            username=username,
        )
