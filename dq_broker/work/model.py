from typing import NamedTuple, Dict

from enum import Enum


class Credentials(NamedTuple):
    username: str
    password: str


class Work(NamedTuple):
    work_id: int
    command: str
    env: Dict[str, str]
    cwd: str
    credentials: Credentials


class WorkEvent(NamedTuple):
    work_id: int
    event_type: str
    work_status: str
    context: Dict[str, str] = {}


class WorkStatus(Enum):
    new = 1
    processing = 2
    finished_with_success = 3
    finished_with_failure = 4
    to_be_killed = 5
    killed = 6
    not_killed = 7
    waiting_for_reschedule = 8
    server_shutdown = 9


ALL_WORK_STATUSES = [e.name for e in WorkStatus]
FINAL_STATUSES = [
    WorkStatus.finished_with_success.name,
    WorkStatus.finished_with_failure.name,
    WorkStatus.killed.name,
]
