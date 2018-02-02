from yawsm.user.actions.list.usecase import ListUserUsecase
from yawsm.user.actions.new.usecase import NewUserUsecase


def new_user_usecase(c):
    return NewUserUsecase(
        user_repo=c('user_repo'),
    )


def list_user_usecase(c):
    return ListUserUsecase(
        user_repo=c('user_repo'),
    )


def register(c):
    c.add_service(new_user_usecase, 'actions.user.new')
    c.add_service(list_user_usecase, 'actions.user.list')
