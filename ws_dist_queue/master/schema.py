from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types.compound import DictType

from ws_dist_queue.master.infrastructure.db.work import ALL_WORK_STATUSES


class WorkIsDoneSchema(Model):
    work_id = IntType(required=True)
    status = StringType(
        required=True,
        choices=ALL_WORK_STATUSES
    )
    output = StringType()


class NewWorkSchema(Model):
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(StringType, default={})


class WorkIdSchema(Model):
    work_id = IntType(required=True)
