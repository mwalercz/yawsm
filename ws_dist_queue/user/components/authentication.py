from ws_dist_queue.user.components.cookie_keeper import CookieKeeper
from ws_dist_queue.user.exceptions import NoCookieException


class Authentication:
    def __init__(self, cookie_keeper: CookieKeeper, parent_pid):
        self.cookie_keeper = cookie_keeper
        self.parent_pid = parent_pid

    def get_headers(self, credentials):
        if credentials.are_correct():
            return credentials.to_dict()
        else:
            cookie = self.cookie_keeper.get_cookie()
            if cookie:
                return {
                    'x-cookie': cookie,
                    'x-parent-pid': self.parent_pid,
                }
            else:
                raise NoCookieException()


class Credentials:
    def __init__(self, username, password, parent_pid):
        self.username = username
        self.password = password
        self.parent_pid = parent_pid

    def are_correct(self):
        return self.password and self.username

    def to_dict(self):
        return dict(
            username=self.username,
            password=self.password,
            parent_pid=self.parent_pid,
        )
