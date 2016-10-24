WORKER_TO_MASTER_PROTOCOL = [
    'worker_up',
    'worker_down',
    'job_started',
    'job_finished',
]

CLIENT_TO_MASTER_PROTOCOL = [
    'new_job',
    'kill_job',
    'list_job',
]

class MasterController:
    def worker_up(self, req):
        pass
    def worker_down(self, req):
        pass
    def job_started(self, req):
        pass
    def job_finished(self, req):
        pass
    def new_job(self, req):
        payload = json.dumps(job_accepted).encode('utf8')
        self.sendMessage(payload)
    def kill_job(self, req):
        pass
    def list_job(self, req):
        pass
