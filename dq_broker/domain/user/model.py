class User:
    def __init__(
            self,
            user_id: int,
            username: str,
            password: str,
            is_admin: bool,
    ):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'is_admin': self.is_admin,
        }

    @classmethod
    def from_dict(cls, raw):
        return cls(**raw)

    @classmethod
    def from_session(cls, session):
        return cls.from_dict(session['user'])
