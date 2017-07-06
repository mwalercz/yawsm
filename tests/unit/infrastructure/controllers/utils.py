from unittest.mock import sentinel

from dq_broker.infrastructure.message import IncomingMessage

from dq_broker.infrastructure.services.request import Request


def create_request(message_body, message_path='some-path'):
    return Request(
            peer=sentinel.peer,
            sender=sentinel.sender,
            message=IncomingMessage(
                path=message_path,
                body=message_body
            )
        )
