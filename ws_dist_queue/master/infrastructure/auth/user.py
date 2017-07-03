import time

import paramiko
from paramiko import SSHClient

from ws_dist_queue.master.exceptions import AuthenticationFailed, RoleNotFound
from ws_dist_queue.master.infrastructure.auth.base import Role


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class SecurityInfo:
    def __init__(self, cookie, parent_pid):
        self.cookie = cookie
        self.parent_pid = parent_pid


class UserSession:
    def __init__(self, credentials, security_info):
        self.credentials = credentials
        self.security_info = security_info


class UserAuthenticationService:
    ROLE = Role.user

    def __init__(self):
        self.sessions = {}
        self.long_sessions = {}

    def authenticate(self, headers, peer):
        try:
            username, password, parent_pid = (
                headers['username'], headers['password'], headers['x-parent-pid'])
        except KeyError:
            try:
                cookie, parent_pid = headers['x-cookie'], headers['x-parent-pid']
            except KeyError:
                raise AuthenticationFailed('Cookie is old or incorrect')
            cookie = self._recreate_session_from_cookie_or_raise(
                cookie, parent_pid, peer
            )
            return {
                'x-cookie': cookie
            }
        cookie = self._create_session_or_raise(
            username, password, parent_pid, peer
        )
        return {
            'x-cookie': cookie
        }

    def get_role(self, peer):
        try:
            self.sessions[peer]
        except BaseException:
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

    def get_credentials(self, peer):
        return self.get_session(peer).credentials

    def get_username(self, peer):
        return self.get_credentials(peer).username

    def _create_session_or_raise(self, username, password, parent_pid, peer):
        self._login_or_raise(username, password)
        cookie = self._create_cookie()
        session = UserSession(
            security_info=SecurityInfo(cookie, parent_pid),
            credentials=Credentials(username, password),
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
        except BaseException:
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
