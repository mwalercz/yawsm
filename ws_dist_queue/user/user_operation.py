class UserOperation:

    def __init__(self):
        self.mapping = {
            'work': self.work,
            'ls': self.list_work,
            'kill': self.kill_work,
        }

    def resolve(self, user_operation):
        return self.mapping['user_operation']



    def work(self):
        pass