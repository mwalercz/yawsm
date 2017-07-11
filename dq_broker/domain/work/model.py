import uuid
from enum import Enum


class Work:
    def __init__(self, work_id, command_data, credentials):
        self.work_id = work_id
        self.command_data = command_data
        self.credentials = credentials

    def to_flat_dict(self):
        return {
            'work_id': self.work_id,
            'command': self.command_data.command,
            'env': self.command_data.env,
            'cwd': self.command_data.cwd,
            'username': self.credentials.username,
            'password': self.credentials.password,
        }

    def set_id(self, work_id):
        self.work_id = work_id

    def __eq__(self, other):
        if not isinstance(other, Work):
            return False
        if self.work_id:
            return self.work_id == other.work_id

        return (
            self.command_data == other.command_data
            and self.credentials == other.credentials
        )

    @classmethod
    def new(cls, command_data, credentials):
        return cls(
            work_id=None,
            command_data=command_data,
            credentials=credentials,
        )


class CommandData:
    def __init__(self, command, env, cwd):
        self.command = command
        self.env = env
        self.cwd = cwd

    def __eq__(self, other):
        if not isinstance(other, CommandData):
            return False
        return (
            self.command == other.command
            and self.env == other.env
            and self.cwd == other.cwd
        )


class WorkStatus(Enum):
    new = 1
    processing = 2
    finished_with_success = 3
    finished_with_failure = 4
    to_be_killed = 5
    killed = 6
    not_killed = 7
    waiting_for_reschedule = 8


class WorkEvent:
    def __init__(self, work_id, event_type, work_status, context=None):
        self.work_id = work_id
        self.event_type = event_type
        self.work_status = work_status
        self.context = context or {}


ALL_WORK_STATUSES = [e.name for e in WorkStatus]
FINAL_STATUSES = [
    WorkStatus.finished_with_success.name,
    WorkStatus.finished_with_failure.name,
    WorkStatus.killed.name,
]
