import time

from ws_dist_queue.master.exceptions import AuthenticationFailed, RoleNotFound, SessionNotFound
from ws_dist_queue.master.infrastructure.auth.base import Role


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        if not isinstance(other, Credentials):
            return False
        else:
            return (
                self.username == other.username
                and self.password == other.password
            )


class SecurityInfo:
    def __init__(self, cookie, parent_pid):
        self.cookie = cookie
        self.parent_pid = parent_pid

    def __eq__(self, other):
        if not isinstance(other, SecurityInfo):
            return False
        else:
            return (
                self.cookie == other.cookie
                and self.parent_pid == other.parent_pid
            )


class UserSession:
    def __init__(self, credentials, security_info, role):
        self.credentials = credentials
        self.security_info = security_info
        self.role = role

    def __eq__(self, other):
        if not isinstance(other, UserSession):
            return False
        else:
            return (
                self.credentials == other.credentials
                and self.security_info == other.security_info
                and self.role == other.role
            )

    @property
    def cookie(self):
        return self.security_info.cookie

    def set_cookie(self, cookie):
        self.security_info.cookie = cookie


class CookieMaker:
    def make(self):
        return str(time.time())


class Validator:
    def is_valid(self, session_security_info, cookie, parent_pid):
        return (
            session_security_info.cookie == cookie and
            session_security_info.parent_pid == parent_pid
        )


class UserAuthenticationService:
    ROLE = Role.user

    def __init__(self, ssh_service, cookie_maker, validator):
        self.ssh_service = ssh_service
        self.cookie_maker = cookie_maker
        self.validator = validator
        self.sessions = {}
        self.long_sessions = {}

    def authenticate(self, headers, peer):
        try:
            self._create_session_or_raise(
                username=headers['username'],
                password=headers['password'],
                parent_pid=headers['x-parent-pid'],
                peer=peer,
            )
        except KeyError:
            try:
                self._recreate_session_from_cookie_or_raise(
                    cookie=headers['x-cookie'],
                    parent_pid=headers['x-parent-pid'],
                    peer=peer,
                )
            except KeyError:
                raise AuthenticationFailed('Cookie is old or incorrect')

    def remove(self, peer):
        try:
            session = self.sessions.pop(peer)
            self.long_sessions.update({
                session.cookie: session
            })
        except KeyError:
            pass

    def get_session(self, peer):
        try:
            return self.sessions[peer]
        except KeyError:
            raise SessionNotFound(peer)

    def get_headers(self, peer):
        return {'x-cookie': self.get_session(peer).cookie}

    def get_credentials(self, peer):
        return self.get_session(peer).credentials

    def get_username(self, peer):
        return self.get_credentials(peer).username

    def get_role(self, peer):
        return self.get_session(peer).role

    def _create_session_or_raise(self, username, password, parent_pid, peer):
        if not self.ssh_service.try_to_login(username, password):
            raise AuthenticationFailed()
        cookie = self.cookie_maker.make()
        session = UserSession(
            security_info=SecurityInfo(cookie, parent_pid),
            credentials=Credentials(username, password),
            role=self.ROLE,
        )
        self.sessions.update({peer: session})

    def _recreate_session_from_cookie_or_raise(self, cookie, parent_pid, peer):
        try:
            session = self.long_sessions.pop(cookie)
        except KeyError:
            raise AuthenticationFailed()
        else:
            self._check_if_valid_or_raise(
                session_security_info=session.security_info,
                cookie=cookie,
                parent_pid=parent_pid,
            )
            self.sessions.update({peer: session})

    def _check_if_valid_or_raise(
            self, session_security_info, cookie, parent_pid
    ):
        if not self.validator.is_valid(
                session_security_info, cookie, parent_pid
        ):
            raise AuthenticationFailed()
