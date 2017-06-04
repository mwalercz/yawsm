import os


class CookieKeeper:
    ENCODING = 'utf8'

    def __init__(self, secret_folder, cookie_filename):
        self._secret_folder = secret_folder
        self._cookie_filename = cookie_filename

    def save(self, cookie):
        user_filepath = self._get_user_filepath()
        if not os.path.exists(user_filepath):
            os.makedirs(user_filepath)
        with open(self._get_cookie_filepath(), mode='w', encoding=self.ENCODING) as f:
            f.write(cookie)

    def get_cookie(self):
        cookie_filepath = self._get_cookie_filepath()
        if not os.path.exists(cookie_filepath):
            return None
        else:
            with open(cookie_filepath, encoding=self.ENCODING) as f:
                return f.readline().strip()

    def _get_cookie_filepath(self):
        return os.path.join(self._get_user_filepath(), self._cookie_filename)

    def _get_user_filepath(self):
        return os.path.join(os.environ['HOME'], self._secret_folder)
