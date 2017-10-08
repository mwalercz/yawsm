from schematics import Model
from schematics.types import StringType, DictType


class NewWorkDto(Model):
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(StringType, default={})
