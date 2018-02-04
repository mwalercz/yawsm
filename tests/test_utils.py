from yawsm.infrastructure.utils import clear_passwords_from_message


def test_clear_passwords_from_message():
    message = {
        'path': 'some-path',
        'body': {
            'username': 'some-user',
            'password': 'some-pass'
        }
    }
    assert clear_passwords_from_message(message) == {
        'path': 'some-path',
        'body': {
            'username': 'some-user',
            'password': '***'
        }
    }


def test_clear_passwords_from_message_empty_body():
    message = {
        'path': 'some-path',
        'body': None
    }
    assert clear_passwords_from_message(message) == {
        'path': 'some-path',
        'body': None
    }
