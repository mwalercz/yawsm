from ws_dist_queue.master.exceptions import AuthenticationFailed, RoleNotFound, SessionNotFound
from ws_dist_queue.master.infrastructure.auth.base import Role


class WorkerAuthenticationService:
    ROLE = Role.worker

    def __init__(self, api_key):
        self.api_key = api_key
        self.connected_peers = set()

    def authenticate(self, headers, peer):
        if self.api_key == headers.get('x-api-key'):
            self.connected_peers.add(peer)
        else:
            raise AuthenticationFailed()

    def get_headers(self, peer):
        return {}

    def get_role(self, peer):
        if peer in self.connected_peers:
            return self.ROLE
        else:
            raise SessionNotFound(peer)

    def remove(self, peer):
        try:
            self.connected_peers.remove(peer)
        except KeyError:
            pass
