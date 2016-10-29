from ws_dist_queue.model.work import JobStatus


class WorkerFactory:
    def __init__(self, job_repo):
        self.job_repo = job_repo

    def make(self, **kwargs):
        return Worker(
            job_repo=self.job_repo,
            **kwargs
        )


class Worker:
    def __init__(self, address, status, current_job=None):
        self.address = address
        self.status = status
        self.current_job = current_job

    @property
    def is_busy(self):
        return bool(self.current_job)

    def assign_job(self, job):
        self.current_job = job
        self.current_job.status = JobStatus.PROCESSING
        self.current_job.worker = self


class WorkerStatus:
    UP = 'up'
    DOWN = 'down'
