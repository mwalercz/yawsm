import uuid
from enum import Enum


class Work:
    def __init__(self, work_id, command_data, credentials):
        self.work_id = work_id
        self.command_data = command_data
        self.credentials = credentials

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
