import jsonpickle
import re

ENCODING = 'utf8'


class MessageSender:
    def __init__(self, message_from, serializer=None, converter=None):
        self.headers = {
            'message_from': message_from,
        }
        self.serializer = serializer or JsonSerializer()
        self.converter = converter or CamelCaseIntoUnderScoreConverter()

    def send(self, recipient, message_body, message_headers={}):
        headers = {k: v for k, v in self.headers.items()}
        headers.update(message_headers)
        headers.update({
            'message_type': self.get_message_type(message_body)
        })

        whole_message = {
            'headers': headers,
            'body': message_body,
        }
        serialized_message = self.serializer.serialize(whole_message)
        recipient.sendMessage(serialized_message)

        msg = 'message: {}, to: {}'.format(whole_message, recipient.peer)
        print(msg)

    def get_message_type(self, message_body):
        return self.converter.to_underscore(type(message_body).__name__)

    def update_cookie(self, cookie):
        self.headers['cookie'] = cookie


class JsonSerializer:
    def serialize(self, message):
        serialized_message = jsonpickle.encode(message)
        return serialized_message.encode(ENCODING)


class JsonDeserializer:
    def deserialize(self, message):
        return jsonpickle.decode(message.decode(ENCODING))


class CamelCaseIntoUnderScoreConverter:
    FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
    ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')
    MESSAGE_LEN = len('_message')

    def to_underscore(self, name):
        s1 = self.FIRST_CAP_RE.sub(r'\1_\2', name)
        s2 = self.ALL_CAP_RE.sub(r'\1_\2', s1).lower()
        return s2[:len(s2) - self.MESSAGE_LEN]