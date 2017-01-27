def validate(schema):
    def validate_decorator(func):
        async def func_wrapper(self, req):
            schema_instance = schema(req.message['body'])
            schema_instance.validate()
            req.validated = schema_instance
            await func(self, req)
        return func_wrapper
    return validate_decorator