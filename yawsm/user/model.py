from typing import NamedTuple


class User(NamedTuple):
    user_id: int
    username: str
    password: str
    is_admin: bool

    @classmethod
    def from_session(cls, session):
        return cls(**session['user'])
