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


STATUS_CODE_MAPPING = {
    200: 'OK',
    202: 'Accepted',
    400: 'Bad Arguments',
    404: 'Not Found',
    500: 'Server Internal Error',
}


class Response:
    def __init__(self, path, status_code=200, body=None):
        self.status_code = status_code
        self.body = body
        self.path = path

    def to_message(self):
        return {
            'headers': {
                'path': self.path,
                'status_code': self.status_code,
                'status_description': STATUS_CODE_MAPPING.get(self.status_code, 'Unknown Error'),
            },
            'body': self.body,
        }

    def __str__(self):
        return '<Response: {}>'.format(str(self.to_message()))

    def __eq__(self, other):
        if not isinstance(other, Response):
            return False
        return self.to_message() == other.to_message()
