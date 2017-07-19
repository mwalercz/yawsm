from schematics.exceptions import DataError

import dq_broker.exceptions


def validate(data, schema):
    schema_instance = schema(data)
    try:
        schema_instance.validate()
        return schema_instance
    except DataError as exc:
        raise dq_broker.exceptions.ValidationError(
            data=exc.to_primitive()
        )
