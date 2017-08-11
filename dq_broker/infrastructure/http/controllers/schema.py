from schematics.models import Model
from schematics.types import StringType, IntType, DictType


class WorkIdSchema(Model):
    work_id = IntType(required=True)


class UsernameSchema(Model):
    username = StringType(required=True)


class NewWorkSchema(Model):
    command = StringType(required=True)
    cwd = StringType(required=True)
    env = DictType(StringType, default={})
