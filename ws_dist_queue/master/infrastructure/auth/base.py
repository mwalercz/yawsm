from enum import Enum

from ws_dist_queue.master.exceptions import AuthenticationFailed, SessionNotFound


class AuthenticationService:
    def __init__(self):
        self.auth_services = []

    def register(self, auth_instance):
        self.auth_services.append(auth_instance)

    def authenticate(self, peer, headers):
        for auth in self.auth_services:
            try:
                auth.authenticate(peer, headers)
                return
            except AuthenticationFailed:
                continue

        raise AuthenticationFailed()

    def get_role(self, peer):
        for auth in self.auth_services:
            try:
                return auth.get_role(peer)
            except SessionNotFound:
                continue

        raise SessionNotFound(peer)

    def get_headers(self, peer):
        for auth in self.auth_services:
            try:
                return auth.get_headers(peer)
            except SessionNotFound:
                continue

        raise SessionNotFound(peer)

    def remove(self, peer):
        for auth in self.auth_services:
            auth.remove(peer)


class Role(Enum):
    user = 1
    worker = 2
    admin = 3


ALL_ROLES = [e for e in Role]
ADMIN_ROLES = [Role.admin]
USER_ROLES = [Role.admin, Role.user]
WORKER_ROLES = [Role.worker]
