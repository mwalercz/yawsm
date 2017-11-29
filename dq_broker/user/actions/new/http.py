from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from schematics import Model
from schematics.types import StringType, BooleanType

from dq_broker.infrastructure.auth.permits import auth_required, admin_only
from dq_broker.infrastructure.http.validator import validate
from dq_broker.infrastructure.repositories.user import UserAlreadyExists
from dq_broker.user.actions.new.usecase import NewUserUsecase


class NewUserDto(Model):
    username = StringType(required=True)
    is_admin = BooleanType(required=False, default=False)


class NewUserController:
    def __init__(self, usecase: NewUserUsecase):
        self.usecase = usecase

    @auth_required
    @admin_only
    async def handle(self, request):
        data = await request.json()
        new_user_dto = validate(data, schema=NewUserDto)
        try:
            result = await self.usecase.perform(new_user_dto)
            return web.json_response(
                result,
                status=201,
            )
        except UserAlreadyExists as exc:
            raise HTTPBadRequest(
                reason='user already exists. username: "{}"'.format(exc.username)
            )

