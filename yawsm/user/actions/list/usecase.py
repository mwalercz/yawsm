from yawsm.infrastructure.repositories.user import UserRepository


class ListUserUsecase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def perform(self):
        users = await self.user_repo.find_all()
        return {
            'users': [self._format(user) for user in users]
        }

    def _format(self, user):
        return {
            'user_id': user.user_id,
            'username': user.username,
            'is_admin': user.is_admin,
        }