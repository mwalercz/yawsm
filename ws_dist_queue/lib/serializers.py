import json


ENCODING = 'utf8'


class JsonSerializer:
    def serialize(self, message):
        return json.dumps(message).encode(ENCODING)

    def pretty(self, message):
        return json.dumps(message, indent=4).encode(ENCODING)


class JsonDeserializer:
    def deserialize(self, message):
        return json.loads(message.decode(ENCODING))
