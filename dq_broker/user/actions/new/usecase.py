from dq_broker.infrastructure.repositories.user import UserRepository


class NewUserUsecase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def perform(self, user_dto):
        user = await self.user_repo.create(user_dto)
        return self._format(user)

    def _format(self, user):
        return {
            'user_id': user.user_id,
            'username': user.username,
            'is_admin': user.is_admin,
        }

