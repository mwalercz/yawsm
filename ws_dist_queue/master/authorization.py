import time

import paramiko
from paramiko import SSHClient


class AuthService:
    def __init__(self, conf, user_auth=None, worker_auth=None):
        self.user_auth = user_auth or UserAuthService()
        self.worker_auth = worker_auth or WorkerAuthService(conf=conf)

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
            session = UserSession(
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
    def __init__(self, conf):
        self.api_key = conf.API_KEY

    def authenticate(self, headers):
        if self.api_key == headers['api_key']:
            return WorkerSession(
                cookie=self.api_key
            )
        else:
            return None

    def get_session(self, cookie):
        return WorkerSession(
                cookie=cookie
        )


class UserSession:
    def __init__(self, cookie, username, password):
        self.cookie = cookie
        self.username = username
        self.password = password


class WorkerSession:
    def __init__(self, cookie):
        self.cookie = cookie