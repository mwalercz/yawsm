import logging

log = logging.getLogger(__name__)


class ResponseClient:
    def __init__(self, serializer):
        self.serializer = serializer

    def send(self, recipient, response):
        message = response.to_dict()
        serialized_message = self.serializer.serialize(message)
        recipient.sendMessage(serialized_message)


class WorkerClient:
    def __init__(self, serializer):
        self.serializer = serializer

    def send(self, recipient, action_name, body=None):
        message = {
            'path': action_name,
            'body': body,
        }
        serialized_message = self.serializer.serialize(message)
        recipient.sendMessage(serialized_message)
        log.info('Message to :"%s" was sent. Body :"%s"', recipient.peer, message)
