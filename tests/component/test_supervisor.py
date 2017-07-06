from unittest.mock import sentinel

import pytest

from dq_broker.infrastructure.message import IncomingMessage

pytestmark = pytest.mark.asyncio


@pytest.fixture
def supervisor(container):
    return container('supervisor')


class TestWorkerFlows:
    async def test_worker_authenticate_connect_requests_work_and_disconnect(
            self, auth, worker_headers, supervisor
    ):
        worker_peer = 'worker-peer'
        auth.authenticate(worker_peer, worker_headers)
        await supervisor.handle_message(
            peer=worker_peer,
            sender=sentinel.sender,
            message=IncomingMessage.from_raw({
                'path': 'worker_connected'
            })
        )
        await supervisor.handle_message(
            peer=worker_peer,
            sender=sentinel.sender,
            message=IncomingMessage.from_raw({
                'path': 'worker_requests_work'
            })
        )
        response = await supervisor.handle_message_and_catch_exceptions(
            peer=worker_peer,
            sender=sentinel.sender,
            message=IncomingMessage.from_raw({
                'path': 'worker_disconnected'
            })
        )
        auth.remove(worker_peer)

        assert response is None

    async def test_user_authenticate_and_new_work(
            self, auth, user_headers, supervisor
    ):
        user_peer = 'user-peer'

        auth.authenticate(user_peer, user_headers)
        response = await supervisor.handle_message_and_catch_exceptions(
            peer=user_peer,
            sender=sentinel.sender,
            message=IncomingMessage.from_raw({
                'path': 'new_work',
                'body': {
                    'command': 'ls',
                    'cwd': '/home'
                }
            })
        )
        assert response.status_code == 202

        response = await supervisor.handle_message_and_catch_exceptions(
            peer=user_peer,
            sender=sentinel.sender,
            message=IncomingMessage.from_raw({
                'path': 'user_disconnected',
            })
        )
        assert response.status_code == 404
        auth.remove(user_peer)

