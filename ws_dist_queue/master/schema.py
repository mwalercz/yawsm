from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types.compound import DictType

from ws_dist_queue.master.models.work import ALL_WORK_STATUSES


class WorkIsDoneSchema:
    work_id = IntType()
    status = StringType(choices=ALL_WORK_STATUSES)


class NewWorkSchema(Model):
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(StringType)


class WorkIdSchema(Model):
    work_id = IntType(required=True)

