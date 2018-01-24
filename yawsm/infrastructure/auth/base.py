import base64
import binascii

from yawsm.work.model import Credentials

AUTHORIZATION_ENCODING = 'latin1'  # this is requests Basic Auth encoding


class BasicAuthExtractionFailed(Exception):
    pass


def basic_auth_extract_credentials(headers, encoding=AUTHORIZATION_ENCODING):
    try:
        authorization = headers['authorization']
    except KeyError:
        raise BasicAuthExtractionFailed('No Authorization header')

    splitted_authorization = authorization.split(' ')

    if len(splitted_authorization) != 2:
        raise BasicAuthExtractionFailed('Wrong Authorization header, it should have two words')

    if splitted_authorization[0] != 'Basic':
        raise BasicAuthExtractionFailed('Wrong Authorization header, no "Basic" word')

    try:
        creds = base64.b64decode(splitted_authorization[1]).split(b':')
    except binascii.Error:
        raise BasicAuthExtractionFailed('B64 decoding failed')

    if len(creds) != 2:
        raise BasicAuthExtractionFailed('Not correct Basic Auth')

    return Credentials(
        username=creds[0].decode(encoding),
        password=creds[1].decode(encoding),
    )
