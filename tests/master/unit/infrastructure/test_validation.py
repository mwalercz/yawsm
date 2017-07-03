from unittest.mock import Mock

import pytest
from schematics.exceptions import DataError

from ws_dist_queue.master import exceptions
from ws_dist_queue.master.infrastructure.request import Request
from ws_dist_queue.master.infrastructure.validation import validate
from ws_dist_queue.master.schema import WorkIsDoneSchema

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
            'status': 'finished_with_success',
            'output': 'some output'
        }
        request = Request(
            message={
                'headers': {},
                'body': data
            },
            sender=Mock(),
            peer=Mock(),
            route=Mock()
        )

        result = await SomeClass().method(request)

        assert result == data

    async def test_input_does_not_match_schema_error_should_be_raised(self):
        request = Request(
            message={
                'headers': {},
                'body': None
            },
            sender=Mock(),
            peer=Mock(),
            route=Mock()
        )
        with pytest.raises(exceptions.ValidationError) as exc:
            await SomeClass().method(request)

        assert exc.value.data == {
            'work_id': ['This field is required.'],
            'status': ['This field is required.'],
        }
