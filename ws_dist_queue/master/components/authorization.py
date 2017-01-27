import time

import paramiko
from paramiko import SSHClient


class AuthenticationFailed(Exception):
    pass


class RoleNotFound(Exception):
    pass


class Authorization:
    def __init__(self):
        self.authorizations = []

    def register(self, auth_instance):
        self.authorizations.append(auth_instance)

    def authenticate(self, headers, peer):
        for auth in self.authorizations:
            try:
                return auth.authenticate(headers, peer)
            except AuthenticationFailed:
                continue

        raise AuthenticationFailed()

    def get_role(self, peer):
        for auth in self.authorizations:
            try:
                return auth.get_role(peer)
            except RoleNotFound:
                continue

        raise RoleNotFound('Peer was not found.')

    def remove(self, peer):
        for auth in self.authorizations:
            auth.remove(peer)


class UserAuthorization:
    ROLE = 'user'

    def __init__(self):
        self.sessions = {}
        self.long_sessions = {}

    def authenticate(self, headers, peer):
        try:
            username, password, parent_pid = (
                headers['username'], headers['password'], headers['parent_pid']
            )
        except KeyError:
            try:
                cookie, parent_pid = headers['x-cookie'], headers['parent_pid']
            except KeyError:
                raise AuthenticationFailed('Cookie is old or incorrect')
            else:
                cookie = self._recreate_session_from_cookie_or_raise(
                    cookie, parent_pid, peer
                )
                return {
                    'x-cookie': cookie
                }
        else:
            cookie = self._create_session_or_raise(
                username, password, parent_pid, peer
            )
            return {
                'x-cookie': cookie
            }

    def get_role(self, peer):
        try:
            self.sessions[peer]
        except:
            raise RoleNotFound()
        else:
            return self.ROLE

    def remove(self, peer):
        try:
            session = self.sessions.pop(peer)
        except KeyError:
            pass
        else:
            cookie = session.cookie
            self.long_sessions.update({
                cookie: session
            })

    def get_session(self, peer):
        try:
            return self.sessions[peer]
        except KeyError:
            raise AuthenticationFailed()

    def _create_session_or_raise(self, username, password, parent_pid, peer):
        self._login_or_raise(username, password)
        cookie = self._create_cookie()
        session = UserSession(
            cookie=cookie,
            username=username,
            password=password,
            parent_pid=parent_pid,
        )
        self.sessions.update({
            peer: session
        })
        return cookie

    def _login_or_raise(self, username, password):
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname='localhost',
                username=username,
                password=password,
            )
        except:
            raise AuthenticationFailed()
        finally:
            if client:
                client.close()

    def _create_cookie(self):
        return str(time.time())

    def _recreate_session_from_cookie_or_raise(self, cookie, parent_pid, peer):
        try:
            session = self.long_sessions.pop(cookie)
        except KeyError:
            raise AuthenticationFailed()
        else:
            self._check_if_valid_or_raise(
                session, cookie, parent_pid, peer
            )
            session.cookie = self._create_cookie()
            self.sessions.update({
                peer: session
            })
            return session.cookie

    def _check_if_valid_or_raise(self, session, cookie, parent_id, peer):
        if not (
            session.cookie == cookie and
            session.parent_pid == parent_id
        ):
            raise AuthenticationFailed()


class WorkerAuthorization:
    ROLE = 'worker'

    def __init__(self, api_key):
        self.api_key = api_key
        self.connected_peers = set()

    def authenticate(self, headers, peer):
        if self.api_key == headers.get('x-api-key'):
            self.connected_peers.add(peer)
            return None
        else:
            raise AuthenticationFailed()

    def get_role(self, peer):
        if peer in self.connected_peers:
            return self.ROLE
        else:
            raise RoleNotFound()

    def remove(self, peer):
        try:
            self.connected_peers.remove(peer)
        except KeyError:
            pass


class UserSession:
    def __init__(self, cookie, username, password, parent_pid):
        self.cookie = cookie
        self.username = username
        self.password = password
        self.parent_pid = parent_pid

