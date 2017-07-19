from schematics import Model
from schematics.types import IntType, StringType, DictType

from dq_broker.domain.work.model import ALL_WORK_STATUSES


class WorkIsDoneSchema(Model):
    work_id = IntType(required=True)
    status = StringType(
        required=True,
        choices=ALL_WORK_STATUSES
    )
    output = StringType()


class WorkerHasWorkSchema(Model):
    work_id = IntType(required=True)
    username = StringType(required=True)
    password = StringType(required=True)
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(field=StringType, required=True)
