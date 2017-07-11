import pytest

from dq_broker.exceptions import ValidationError
from infrastructure.websocket.message import IncomingMessage


class TestIncomingMessage:
    def test_valid_raw_message_1(self):
        raw_message = {
            'path': 'some-path'
        }

        message = IncomingMessage.from_raw(raw_message)

        assert message.path == 'some-path'
        assert message.body == {}

    def test_valid_raw_message_2(self):
        raw_message = {
            'path': 'some-path',
            'body': {'key': 'value'}
        }

        message = IncomingMessage.from_raw(raw_message)

        assert message.path == 'some-path'
        assert message.body == {'key': 'value'}

    def test_invalid_raw_message_1(self):
        raw_message = {
            'body': 'some-body'
        }

        with pytest.raises(ValidationError):
            IncomingMessage.from_raw(raw_message)

    def test_invalid_raw_message_2(self):
        raw_message = {
            'path': None,
            'body': 'some-body'
        }

        with pytest.raises(ValidationError):
            IncomingMessage.from_raw(raw_message)

