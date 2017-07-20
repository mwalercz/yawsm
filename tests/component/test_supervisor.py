from unittest.mock import sentinel

import pytest

from dq_broker.infrastructure.websocket.message import IncomingMessage

pytestmark = pytest.mark.asyncio


@pytest.fixture
def supervisor(container):
    return container('supervisor')


class TestWorkerFlows:
    async def test_worker_authenticate_connect_requests_work_and_disconnect(
            self, worker_auth, worker_headers, supervisor
    ):
        worker_peer = 'worker-peer'
        await worker_auth.authenticate(worker_headers)
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

        assert response is None
