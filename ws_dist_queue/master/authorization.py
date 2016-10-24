import paramiko
import time
from paramiko import SSHClient


class AuthService:
    def __init__(self, user_auth, worker_auth):
        self.user_auth = user_auth
        self.worker_auth = worker_auth

    def authenticate(self, message):
        if message['from'] == 'client':
            return self.user_auth.authenticate(message)
        elif message['from'] == 'worker':
            return self.worker_auth.authenticate(message)

    def get_session(self, message_from, cookie):
        if message_from == 'client':
            return self.user_auth.get_session(cookie)
        elif message_from == 'worker':
            return self.worker_auth.get_session(cookie)


class UserAuthService:
    def __init__(self):
        self.authenticated_users = {}

    def authenticate(self, message):
        username, password = message['username'], message['password']
        user = self._try_to_login(username, password)
        if user:
            cookie = self._create_cookie()
            self.authenticated_users.update({
                cookie: Session(
                    cookie=cookie,
                    username=username,
                    password=password,
                )
            })
            return cookie
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

    def authenticate(self, message):
        api_key = message['api_key']
        if self.API_KEY == api_key:
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
