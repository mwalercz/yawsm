class WorkerNotFound(Exception):
    pass


class WorkNotFound(Exception):
    def __init__(self, work_id=None, username=None):
        self.work_id = work_id
        self.username = username


class InvalidArgumentException(Exception):
    pass


class InvalidStateException(Exception):
    pass