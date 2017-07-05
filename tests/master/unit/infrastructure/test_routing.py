from unittest.mock import Mock

import pytest

from ws_dist_queue.master.exceptions import AccessForbidden
from ws_dist_queue.master.infrastructure.auth.base import USER_ROLES, AuthenticationService, Role, ALL_ROLES, \
    WORKER_ROLES
from ws_dist_queue.master.infrastructure.services.routing import Route, Router


@pytest.fixture
def mock_auth():
    return Mock(spec=AuthenticationService)


@pytest.fixture
def default_route():
    return Route(
        path='default',
        controller=Controller(),
        allowed_roles=ALL_ROLES
    )


@pytest.fixture
def router(mock_auth, default_route):
    router = Router(
        auth=mock_auth
    )
    router.register_default(default_route)
    return router


class TestRoute:
    def test_is_allowed_when_peer_role_not_in_allowed_roles(
            self, mock_auth,
    ):
        route = Route(
            path='some-path',
            controller=Mock(),
            allowed_roles=USER_ROLES
        )
        mock_auth.get_role.return_value = Role.worker
        peer = '123.123.123.1:1'
        result = route.can_be_accessed(
            peer, mock_auth
        )

        assert result is False
        mock_auth.get_role.assert_called_once_with(peer)

    def test_is_allowed_when_peer_role_in_allowed_roles(
            self, mock_auth
    ):
        route = Route(
            path='some-path',
            controller=Mock(),
            allowed_roles=USER_ROLES
        )
        mock_auth.get_role.return_value = Role.user

        result = route.can_be_accessed(
            '123.123.123.1:1', mock_auth
        )

        assert result is True


class Controller:
    def handle(self, req):
        return req.body


class TestRouter:
    def test_get_route_given_only_default_accessible_route(
            self, mock_auth, router, default_route
    ):
        mock_auth.get_role.return_value = Role.user

        route = router.get_route('not-existing-path', 'some-peer')

        assert route == default_route

    def test_get_route_given_route_exists_and_is_accessible_to_user(
            self, mock_auth, router
    ):
        mock_auth.get_role.return_value = Role.user
        route = Route('path_one', Controller(), USER_ROLES)
        router.register(route)

        result_route = router.get_route('path_one', 'some-peer')

        assert result_route == route

    def test_get_route_given_route_exists_but_is_not_accessible_to_worker(
            self, mock_auth, router,
    ):
        mock_auth.get_role.return_value = Role.worker
        route = Route('path_one', Controller(), USER_ROLES)
        router.register(route)

        with pytest.raises(AccessForbidden):
            router.get_route('path_one', 'some-peer')

    def test_available_paths_for_user_role(
            self, mock_auth, router,
    ):
        mock_auth.get_role.return_value = Role.user
        user_route = Route('path_user', Controller(), USER_ROLES)
        router.register(user_route)
        worker_route = Route('path_worker', Controller(), WORKER_ROLES)
        router.register(worker_route)

        paths = router.get_available_paths('some-peer')

        assert paths == ['default', 'path_user']




