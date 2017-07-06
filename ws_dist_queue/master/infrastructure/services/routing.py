from ws_dist_queue.master.exceptions import AccessForbidden


class Route:
    def __init__(self, path, controller, allowed_roles):
        self.path = path
        self.controller = controller
        self.allowed_roles = allowed_roles

    @property
    def handler(self):
        return self.controller.handle

    def can_be_accessed(self, peer, auth_service):
        peer_role = auth_service.get_role(peer)
        return peer_role in self.allowed_roles

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False
        else:
            return (
                self.path == other.path and
                self.controller == other.controller and
                self.allowed_roles == other.allowed_roles
            )


class Router:
    def __init__(self, auth):
        self.auth = auth
        self.default_route = None
        self.routes = {}

    def register(self, route):
        self.routes.update({
            route.path: route
        })

    def register_default(self, route):
        self.register(route)
        self.default_route = route

    def get_available_paths(self, peer):
        return [
            path for path, route in self.routes.items()
            if route.can_be_accessed(
                peer=peer,
                auth_service=self.auth,
            )
        ]

    def get_route(self, path, peer):
        route = self.routes.get(path, self.default_route)
        if not route.can_be_accessed(
            peer=peer,
            auth_service=self.auth,
        ):
            msg = 'Peer: "{}" is not allowed to access route: "{}"'.format(
                peer, route.path
            )
            raise AccessForbidden(data=msg)
        else:
            return route
