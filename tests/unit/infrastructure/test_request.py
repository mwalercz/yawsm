from unittest.mock import Mock

import pytest

from yawsm.infrastructure import exceptions
from yawsm.infrastructure.websocket.message import IncomingMessage
from yawsm.infrastructure.websocket.request import Request, validate
from yawsm.worker.actions.work_is_done.ws import WorkIsDoneSchema

pytestmark = pytest.mark.asyncio


class SomeClass:
    @validate(schema=WorkIsDoneSchema)
    async def method(self, req):
        return {
            'work_id': req.validated.work_id,
            'status': req.validated.status,
            'output': req.validated.output
        }


class TestValidate:
    async def test_when_input_matches_schema_no_error_should_be_raised(self):
        data = {
            'work_id': 1,
            'status': 'DONE',
            'output': 'some output'
        }
        request = Request(
            message=IncomingMessage(
                path='something',
                body=data
            ),
            sender=Mock(),
            peer=Mock(),
        )

        result = await SomeClass().method(request)

        assert result == data

    async def test_input_does_not_match_schema_error_should_be_raised(self):
        request = Request(
            message=IncomingMessage(
                path='lala',
                body={},
            ),
            sender=Mock(),
            peer=Mock(),
        )
        with pytest.raises(exceptions.ValidationError) as exc:
            await SomeClass().method(request)

        assert exc.value.data == {
            'work_id': ['This field is required.'],
            'status': ['This field is required.'],
        }
