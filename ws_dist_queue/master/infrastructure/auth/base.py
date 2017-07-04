import time
from enum import Enum

import paramiko
from paramiko import SSHClient

from ws_dist_queue.master.exceptions import AuthenticationFailed, RoleNotFound


class AuthenticationService:
    def __init__(self):
        self.auth_services = []

    def register(self, auth_instance):
        self.auth_services.append(auth_instance)

    def authenticate(self, headers, peer):
        for auth in self.auth_services:
            try:
                return auth.authenticate(headers, peer)
            except AuthenticationFailed:
                continue

        raise AuthenticationFailed()

    def get_role(self, peer):
        for auth in self.auth_services:
            try:
                return auth.get_role(peer)
            except RoleNotFound:
                continue

        raise RoleNotFound('Peer was not found.')

    def remove(self, peer):
        for auth in self.auth_services:
            auth.process_remove_worker(peer)


class Role(Enum):
    user = 1
    worker = 2
    admin = 3


ALL_ROLES = [e for e in Role]
ADMIN_ROLES = [Role.admin]
USER_ROLES = [Role.admin, Role.user]
WORKER_ROLES = [Role.worker]


