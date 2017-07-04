class ValidationError(Exception):
    def __init__(self, data):
        self.data = data


class AccessForbidden(Exception):
    def __init__(self, data):
        self.data = data


class AuthenticationFailed(Exception):
    pass


class RoleNotFound(Exception):
    pass
