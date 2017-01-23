import os


class CookieKeeper:
    COOKIE_FILENAME = 'COOKIE'
    ENCODING = 'utf8'

    def __init__(self, secret_folder):
        self.secret_folder = secret_folder

    def save(self, cookie):
        user_filepath = self.get_user_filepath()
        if not os.path.exists(user_filepath):
            os.makedirs(user_filepath)
        with open(self.get_cookie_filepath(), mode='w', encoding=self.ENCODING) as f:
            f.write(cookie)

    def get_cookie(self):
        cookie_filepath = self.get_cookie_filepath()
        if not os.path.exists(cookie_filepath):
            return None
        else:
            with open(cookie_filepath, encoding=self.ENCODING) as f:
                return f.readline().strip()

    def get_cookie_filepath(self):
        return os.path.join(self.get_user_filepath(), self.COOKIE_FILENAME)

    def get_user_filepath(self):
        return os.path.join(os.environ['HOME'], self.secret_folder)



