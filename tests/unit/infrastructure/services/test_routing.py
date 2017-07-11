from unittest.mock import Mock

import pytest

from dq_broker.exceptions import RouteNotFound
from dq_broker.infrastructure.auth.base import AuthenticationService
from infrastructure.websocket.routing import Route, Router


@pytest.fixture
def mock_auth():
    return Mock(spec=AuthenticationService)


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
