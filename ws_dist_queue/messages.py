from enum import Enum

from schematics.models import Model
from schematics.transforms import blacklist
from schematics.types import StringType, IntType
from schematics.types.compound import DictType, ListType
from ws_dist_queue.model.work import ALL_WORK_STATUSES


class WorkIsDoneModel:
    work_id = IntType()
    status = StringType(choices=ALL_WORK_STATUSES)

class WorkModel(Model):
    work_id = IntType()
    username = StringType()
    password = StringType()
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(StringType)
    class Option:
        roles = {
            'user': blacklist('username', 'password')
        }

class ListWorkResponseMessage(Model):
    work_list = ListType(WorkModel)

class WorkId(Model):
    work_id = IntType(required=True)

class Message(Enum):
    worker_created = 1
    worker_down = 2
    work_is_done = 3
    worker_requests_work = 4
    new_work = 5
    kill_work = 6
    list_work = 7
    work_accepted = 8
    work_accepted_no_worker = 9
    work_to_be_done = 10
    no_work_with_given_id = 11
    list_work_response = 12
    work_is_ready = 13
    work_was_killed = 14

MASTER_MAPPING = {
    Message.worker_created: None,
    Message.worker_down: None,
    Message.work_is_done: WorkIsDoneModel,
    Message.worker_requests_work: None,
    Message.new_work: WorkModel,
    Message.kill_work: WorkId,
    Message.list_work: None,
    Message.work_to_be_done: WorkModel,
}


class NoMessageWithGivenMessageType(Exception):
    pass


class MessageFactory:
    def __init__(self, mapping):
        self.mapping = mapping

    def get_object(self, message_type):
        try:
            return self.mapping[Message[message_type]]
        except KeyError:
            raise NoMessageWithGivenMessageType()
