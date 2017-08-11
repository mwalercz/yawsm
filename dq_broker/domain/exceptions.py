class WorkerNotFound(Exception):
    pass


class WorkNotFound(Exception):
    def __init__(self, work_id=None, user_id=None):
        self.work_id = work_id
        self.username = user_id


class UserNotFound(Exception):
    def __init__(self, username):
        self.username = username


class InvalidArgumentException(Exception):
    pass


class InvalidStateException(Exception):
    pass
