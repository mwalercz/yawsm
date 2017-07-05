from schematics.exceptions import DataError

from ws_dist_queue.master import exceptions


class Request:
    def __init__(self, message, sender, peer, route):
        self.message = message
        self.sender = sender
        self.peer = peer,
        self.route = route

    def get_response(self, status_code=200, body=None):
        return Response(
            path=self.route.path,
            status_code=status_code,
            body=body,
        )

    def to_dict(self):
        return {
            'message': str(self.message),
            'sender': self.sender,
            'peer': self.peer,
            'route': str(self.route),
        }

    def __str__(self):
        return '<Request: {}>'.format(str(self.to_dict()))


STATUS_CODE_MAPPING = {
    200: 'OK',
    202: 'Accepted',
    400: 'Bad Arguments',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Server Internal Error',
}


class Response:
    def __init__(self, path, status_code=200, body=None):
        self.status_code = status_code
        self.body = body
        self.path = path

    def to_dict(self):
        return {
            'headers': {
                'path': self.path,
                'status_code': self.status_code,
                'status_description': STATUS_CODE_MAPPING.get(self.status_code, 'Unknown Error'),
            },
            'body': self.body,
        }

    def __str__(self):
        return '<Response: {}>'.format(str(self.to_dict()))

    def __eq__(self, other):
        if not isinstance(other, Response):
            return False
        return self.to_dict() == other.to_dict()


def validate(schema):
    def validate_decorator(func):
        async def func_wrapper(self, req):
            schema_instance = schema(req.message.body)
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