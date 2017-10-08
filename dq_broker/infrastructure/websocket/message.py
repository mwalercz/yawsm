from dq_broker.infrastructure.exceptions import ValidationError


class IncomingMessage:
    def __init__(self, path, body=None):
        self.path = path
        self.body = body or {}

    @classmethod
    def from_raw(cls, raw_message):
        try:
            path = raw_message['path']
            if path is None:
                raise ValidationError(
                    data={'path': ['Must not be None']}
                )
            return cls(
                path=path,
                body=raw_message.get('body')
            )
        except KeyError:
            raise ValidationError(
                data={'path': ['This field is required']}
            )

    def to_dict(self):
        return {
            'path': self.path,
            'body': self.body,
        }

    def __str__(self):
        return '<IncomingMessage: {}>'.format(str(self.to_dict()))
