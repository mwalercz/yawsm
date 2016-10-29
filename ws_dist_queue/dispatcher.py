class Dispatcher:
    def __init__(self, controller):
        self.controller = controller

    def find_method(self, message_type):
        try:
            responder = getattr(self.controller, message_type)
        except AttributeError:
            raise RuntimeError('Method: {} in controller: {} not implemented'.format(
                message_type,
                str(self.controller)
            ))
        else:
            if callable(responder):
                return responder