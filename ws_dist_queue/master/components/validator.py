def validate(schema):
    def validate_decorator(func):
        async def func_wrapper(self, req):
            schema_instance = schema(req.message['body'])
            schema_instance.validate()
            req.validated = schema_instance
            await func(self, req)
        return func_wrapper
    return validate_decorator




if __name__ == '__main__':
    class TestClass:
        @validate(schema=NewWorkSchema)
        def func(self, req):
            print(req)


    req = Request(
        message={
            'body': {
                'command': 'ls',
                'cwd': 'haha'
            }
        },
        sender=None
    )
    clz = TestClass()
    f = getattr(clz, 'func')
    f(req)
    print(req.validated)
