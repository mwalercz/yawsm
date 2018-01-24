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
    new = 1
    processing = 2
    finished_with_success = 3
    finished_with_failure = 4
    to_be_cancelled = 5
    cancelled = 6
    cancel_failed = 7
    waiting_for_reschedule = 8
    unknown = 9


ALL_STATUSES = {e.name for e in WorkStatus}

FINAL_STATUSES = {
    WorkStatus.finished_with_success.name,
    WorkStatus.finished_with_failure.name,
    WorkStatus.cancelled.name,
}

NON_FINAL_STATUSES = ALL_STATUSES - FINAL_STATUSES

WORK_IN_WORK_QUEUE_STATUSES = {
    WorkStatus.new.name,
    WorkStatus.waiting_for_reschedule.name,
}

WORK_PROCESSED_BY_WORKER_STATUSES = {
    WorkStatus.processing.name,
    WorkStatus.to_be_cancelled.name,
    WorkStatus.cancel_failed.name,
}
