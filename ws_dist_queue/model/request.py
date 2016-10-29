class Request:
    def __init__(self, message, sender, session=None):
        self.message = message
        self.sender = sender
        self.session = session