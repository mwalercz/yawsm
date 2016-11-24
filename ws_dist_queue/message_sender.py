import logging

import re
import json

ENCODING = 'utf8'


class MessageSender:
    log = logging.getLogger(__name__)

    def __init__(self, message_from):
        self.headers = {
            'message_from': message_from,
        }
        self.serializer = JsonSerializer()

    def send(self, recipient, message_type, message_body=None, message_headers={}):
        headers = {k: v for k, v in self.headers.items()}
        headers.update(message_headers)
        headers.update({
            'message_type': message_type.name
        })
        whole_message = {
            'headers': headers,
            'body': message_body,
        }
        serialized_message = self.serializer.serialize(whole_message)
        recipient.sendMessage(serialized_message)

        self.log.info(
            'Message was sent to {peer}. {message}'.format(
                peer=recipient.peer,
                message=whole_message
            )
        )

    def update_cookie(self, cookie):
        self.headers['cookie'] = cookie


class JsonSerializer:
    def serialize(self, message):
        return json.dumps(message).encode(ENCODING)


class JsonDeserializer:
    def deserialize(self, message):
        return json.loads(message.decode(ENCODING))