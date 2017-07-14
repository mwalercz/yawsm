from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types.compound import DictType


class NewWorkSchema(Model):
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(StringType, default={})


class WorkDetailsSchema(Model):
    work_id = IntType(required=True)
    username = StringType(required=True)


class UsernameSchema(Model):
    username = StringType(required=True)
