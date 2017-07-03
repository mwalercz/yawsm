class ResponseClient:
    def __init__(self, serializer):
        self.serializer = serializer

    def send(self, recipient, response):
        message = response.to_message()
        serialized_message = self.serializer.serialize(message)
        recipient.sendMessage(serialized_message)


class WorkerClient:
    def __init__(self, serializer):
        self.serializer = serializer

    def send(self, recipient, action_name, body=None):
        path = action_name
        message = {
            'headers': {
                'path': path,
            },
            'body': body,
        }
        serialized_message = self.serializer.serialize(message)
        recipient.sendMessage(serialized_message)

