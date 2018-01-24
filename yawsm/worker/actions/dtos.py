from schematics.models import Model
from schematics.types import IntType


class WorkIdDto(Model):
    work_id = IntType(required=True)



