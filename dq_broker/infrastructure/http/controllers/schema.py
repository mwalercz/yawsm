from schematics.models import Model
from schematics.types import StringType, IntType


class WorkDetailsSchema(Model):
    work_id = IntType(required=True)
    username = StringType(required=True)


class UsernameSchema(Model):
    username = StringType(required=True)
