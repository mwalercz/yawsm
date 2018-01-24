from schematics.exceptions import DataError

import yawsm.infrastructure.exceptions


def validate(data, schema):
    schema_instance = schema(data)
    try:
        schema_instance.validate()
        return schema_instance
    except DataError as exc:
        raise yawsm.infrastructure.exceptions.ValidationError(
            data=exc.to_primitive()
        )
