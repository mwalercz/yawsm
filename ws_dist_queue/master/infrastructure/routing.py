from ws_dist_queue.master.exceptions import PathDoesNotExist


class Route:
    def __init__(self, path, controller, role):
        self.path = path
        self.controller = controller
        self.role = role

    @property
    def handler(self):
        return self.controller.handle


class Router:
    def __init__(self):
        self.routes = {}

    def register(self, path, controller, role):
        self.routes.update({
            path: Route(path, controller, role)
        })

    def get_route(self, path):
        if path is None:
            return PathDoesNotExist(None)
        try:
            return self.routes[path]
        except KeyError:
            raise PathDoesNotExist(path)
