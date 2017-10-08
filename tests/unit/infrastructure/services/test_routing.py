import pytest

from dq_broker.infrastructure.exceptions import RouteNotFound
from dq_broker.infrastructure.websocket.routing import Route, Router


@pytest.fixture
def router():
    return Router()


class Controller:
    def handle(self, req):
        return req.body


class TestRouter:
    def test_get_route_when_no_routes_available(
            self, router
    ):
        with pytest.raises(RouteNotFound) as exc:
            router.get_route('not-existing-path')

    def test_get_route_when_route_is_available(
            self, router,
    ):
        route = Route('path_one', Controller())
        router.register(route)

        assert router.get_route('path_one') == route
