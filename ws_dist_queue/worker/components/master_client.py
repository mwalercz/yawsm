class MasterClient:
    master = NotImplemented

    def __init__(self, serializer):
        self.path = 'worker'
        self.serializer = serializer

    def send(self, action_name, body=None):
        path = self.path + '/' + action_name
        message = {
            'path': path,
            'body': body,
        }
        serialized_message = self.serializer.serialize(message)
        self.master.sendMessage(serialized_message)