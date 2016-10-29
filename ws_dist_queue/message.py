class MessageFactory:
    def __init__(self, mapping):
        self.mapping = mapping

    def create(self, raw_message):
        headers = raw_message.pop('headers')
        message_type = headers['message_type']
        if len(raw_message) == 0:
            return self.mapping[message_type]
        else:
            return self.mapping[message_type](**raw_message)


class WorkerCreatedMessage:
    pass


class WorkerDownMessage:
    pass


class WorkAcceptedNoWorkersMessage:
    def __init__(self, work_id):
        self.work_id = work_id

class WorkAcceptedMessage:
    def __init__(self, work_id):
        self.work_id = work_id


class JobFinishedMessage:
    def __init__(self, job_id, status):
        self.job_id = job_id
        self.status = status


class WorkMessage:
    def __init__(self, command, cwd, env=None):
        self.command = command
        self.cwd = cwd
        self.env = env


class KillWorkMessage:
    def __init__(self, work_id):
        self.work_id = work_id


class ListWorkMessage:
    pass


class WorkIsDoneMessage:
    pass


class WorkerRequestsWorkMessage:
    pass


class WorkToBeDoneMessage:
    def __init__(self, work):
        self.work = work

class WorkIsReadyMessage:
    pass


class ClientAuthorizedMessage:
    def __init__(self, cookie):
        self.cookie = cookie


MASTER_MAPPING = {
    'worker_created': WorkerCreatedMessage,
    'worker_down': WorkerDownMessage,
    'work_is_done': WorkIsDoneMessage,
    'worker_requests_work': WorkerRequestsWorkMessage,
    'work': WorkMessage,
    'kill_work': KillWorkMessage,
    'list_work': ListWorkMessage,
    'work_to_be_done': WorkToBeDoneMessage,
    'work_accepted': WorkAcceptedMessage,
}