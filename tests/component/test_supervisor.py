from unittest.mock import sentinel

import pytest

from yawsm.infrastructure.websocket.message import IncomingMessage
from yawsm.infrastructure.websocket.request import Request

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
        response = await supervisor.handle_request_and_catch_exceptions(
            Request(
                peer=worker_peer,
                sender=sentinel.sender,
                message=IncomingMessage.from_raw({
                    'path': 'worker_disconnected'
                })
            )
        )

        assert response is None
