from dq_broker.infrastructure.exceptions import RouteNotFound


class Route:
    def __init__(self, path, controller):
        self.path = path
        self.controller = controller

    @property
    def handler(self):
        return self.controller.handle

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False
        else:
            return (
                self.path == other.path and
                self.controller == other.controller
            )


class Router:
    def __init__(self):
        self.routes = {}

    def register(self, route):
        self.routes.update({
            route.path: route
        })

    def get_route(self, path):
        try:
            return self.routes[path]
        except KeyError:
            raise RouteNotFound(path)

