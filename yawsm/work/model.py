from typing import NamedTuple, Dict

from enum import Enum


class Credentials(NamedTuple):
    username: str
    password: str


class KillWork(NamedTuple):
    work_id: int
    user_id: int


class Work(NamedTuple):
    work_id: int
    command: str
    env: Dict[str, str]
    cwd: str
    credentials: Credentials


class WorkEvent(NamedTuple):
    work_id: int
    reason: str
    work_status: str
    context: Dict[str, str] = {}


class WorkStatus(Enum):
    READY = 1
    PROCESSING = 2
    FINISHED = 3
    CANCELLED = 4
    UNKNOWN = 5
    ABANDONED = 6
    ERROR = 7


ALL_STATUSES = {e.name for e in WorkStatus}

FINAL_STATUSES = {
    WorkStatus.FINISHED.name,
    WorkStatus.CANCELLED.name,
}

NON_FINAL_STATUSES = ALL_STATUSES - FINAL_STATUSES
