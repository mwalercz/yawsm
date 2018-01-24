import uuid

import pytest

from yawsm.infrastructure.repositories.user import UserAlreadyExists
from yawsm.user.actions.new.http import NewUserDto
from yawsm.user.actions.new.usecase import NewUserUsecase

pytestmark = pytest.mark.asyncio


class TestCreateUsers:
    @pytest.mark.parametrize('param_is_admin', [
        True, False
    ])
    async def test_new_user(
            self, new_user_usecase: NewUserUsecase, param_is_admin
    ):
        username = str(uuid.uuid4())[:30]
        dto = NewUserDto(dict(username=username, is_admin=param_is_admin))
        user = await new_user_usecase.perform(dto)
        assert user['username'] == username
        assert user['is_admin'] == param_is_admin

    async def test_creating_user_with_same_username_should_fail(
            self, new_user_usecase: NewUserUsecase
    ):
        username = str(uuid.uuid4())[:30]
        is_admin = False
        dto = NewUserDto(dict(username=username, is_admin=is_admin))
        await new_user_usecase.perform(dto)
        with pytest.raises(UserAlreadyExists) as exc:
            await new_user_usecase.perform(dto)

        assert exc.value.username == username

