ENCODING = 'utf8'


class UserClient:
    def __init__(self, serializer):
        self.serializer = serializer

    def send(self, recipient, info, body=None):
        message = {
            'info': info,
            'body': body,
        }
        serialized_message = self.serializer.serialize(message)
        recipient.sendMessage(serialized_message)


class WorkerClient:
    def __init__(self, serializer):
        self.path = 'worker'
        self.serializer = serializer

    def send(self, recipient, action_name, body=None):
        path = self.path + '/' + action_name
        message = {
            path: path,
            body: body,
        }
        serialized_message = self.serializer.serialize(message)
        recipient.sendMessage(serialized_message)


