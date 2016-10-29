import paramiko
import time
from paramiko import SSHClient


class AuthService:
    def __init__(self, user_auth=None, worker_auth=None):
        self.user_auth = user_auth or UserAuthService()
        self.worker_auth = worker_auth or WorkerAuthService()

    def authenticate(self, headers):
        if headers['message_from'] == 'user':
            return self.user_auth.authenticate(headers)
        elif headers['message_from'] == 'worker':
            return self.worker_auth.authenticate(headers)
        else:
            raise RuntimeError()

    def get_session(self, message_from, cookie):
        if message_from == 'user':
            return self.user_auth.get_session(cookie)
        elif message_from == 'worker':
            return self.worker_auth.get_session(cookie)
        else:
            raise RuntimeError()


class UserAuthService:
    def __init__(self):
        self.authenticated_users = {}

    def authenticate(self, headers):
        user = self._try_to_login(headers['username'], headers['password'])
        if user:
            cookie = self._create_cookie()
            session = Session(
                    cookie=cookie,
                    username=headers['username'],
                    password=headers['password'],
                )
            self.authenticated_users.update({
                cookie: session
            })
            return session
        else:
            return None

    def get_session(self, cookie):
        return self.authenticated_users.get(cookie, None)

    def _try_to_login(self, username, password):
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname='localhost',
                username=username,
                password=password,
            )
        except:
            return None
        else:
            return username
        finally:
            if client:
                client.close()

    def _create_cookie(self):
        return str(time.time())


class WorkerAuthService:
    API_KEY = '1111'

    def authenticate(self, headers):
        if self.API_KEY == headers.api_key:
            return self.API_KEY
        else:
            return None

    def get_session(self, cookie):
        return self.API_KEY == cookie


class Session:
    def __init__(self, cookie, username, password):
        self.cookie = cookie
        self.username = username
        self.password = password
