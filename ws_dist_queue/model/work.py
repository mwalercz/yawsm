from enum import Enum


class Work:
    def __init__(
            self, cwd, command, username=None,
            environment=None, work_id=None,
            status=None, password=None
    ):
        self.work_id = work_id
        self.username = username
        self.password = password
        self.cwd = cwd
        self.command = command
        self.environment = environment or {}
        self.status = status


class WorkStatus(Enum):
    received = 1
    processing = 2
    finished_with_success = 2
    finished_with_failure = 3
    work_killed = 4
    worker_failure = 5

ALL_WORK_STATUSES = [e.name for e in WorkStatus]



