from schematics.exceptions import DataError

from ws_dist_queue.master import exceptions


def validate(schema):
    def validate_decorator(func):
        async def func_wrapper(self, req):
            schema_instance = schema(req.message.get('body', {}))
            try:
                schema_instance.validate()
            except DataError as exc:
                raise exceptions.ValidationError(
                    data=exc.to_primitive()
                )
            else:
                req.validated = schema_instance
                return await func(self, req)
        return func_wrapper
    return validate_decorator
