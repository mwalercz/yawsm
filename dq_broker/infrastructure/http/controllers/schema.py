from schematics.models import Model
from schematics.types import StringType, IntType, DictType


class WorkIdDto(Model):
    work_id = IntType(required=True)


class NewWorkDto(Model):
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(StringType, default={})
