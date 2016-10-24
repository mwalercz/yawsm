

MASTER_TO_WORKER_PROTOCOL = [
    'new_job',
    'kill_job'
]


class ServerDispatcher:
    def __init__(self, worker_dispatcher, client_dispatcher):
        self.worker_dispatcher = worker_dispatcher
        self.client_dispatcher = client_dispatcher

    def find_method(self, message_from, message_type):
        if message_from == 'worker':
            return self.worker_dispatcher.find_method(message_type)
        elif message_from == 'client':
            return self.client_dispatcher.find_method(message_type)
        else:
            raise RuntimeError('Message from: {} not supported'.format(
                message_from
            ))


class Dispatcher:
    def __init__(self, controller):
        self.controller = controller

    def find_method(self, message_type):
        try:
            responder = getattr(message_type,  self.controller)
        except AttributeError:
            raise RuntimeError('Method: {} in controller: {} not implemented'.format(
                message_type,
                str(self.controller)
            ))
        else:
            if callable(responder):
                return responder