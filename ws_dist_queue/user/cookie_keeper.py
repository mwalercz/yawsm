from pathlib import Path

import os


class CookieKeeper:
    COOKIE_FILENAME = 'COOKIE'

    def __init__(self, conf):
        self.partial_user_filepath = conf.PARTIAL_USER_FILEPATH
        self.encoding = conf.ENCODING

    def save(self, cookie):
        user_filepath = self.get_user_filepath()
        if not os.path.exists(user_filepath):
            os.makedirs(user_filepath)
        with open(self.get_cookie_filepath(), mode='w', encoding=self.encoding) as f:
            f.write(cookie)

    def get_cookie(self):
        cookie_filepath = self.get_cookie_filepath()
        if not os.path.exists(cookie_filepath):
            return None
        else:
            with open(cookie_filepath, encoding=self.encoding) as f:
                return f.readline().strip()

    def get_cookie_filepath(self):
        return os.path.join(self.get_user_filepath(), self.COOKIE_FILENAME)

    def get_user_filepath(self):
        return os.path.join(os.environ['HOME'], self.partial_user_filepath)

