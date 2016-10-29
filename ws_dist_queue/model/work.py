import colander
from colander import SchemaNode


class Work:
    def __init__(
            self, cwd, command, username=None,
            environment=None, work_id=None,
            status=None, worker=None,
            password=None
    ):
        self.work_id = work_id
        self.username = username
        self.password = password
        self.cwd = cwd
        self.command = command
        self.environment = environment or {}
        self.status = status
        self.worker = worker

    @property
    def is_processed(self):
        return bool(self.worker)

    @staticmethod
    def create(job):
        return Work(
            work_id=job.get_cookie('job_id'),
            username=job.get_cookie('user'),
            cwd=job.get_cookie('cwd'),
            command=job.get_cookie('command'),
            environment=job.get_cookie('environment')
        )



class JobStatus:
    RECEIVED = 'received'
    PROCESSING = 'processing'
    FINISHED_WITH_SUCCESS = 'finished with success'
    FINISHED_WITH_FAILURE = 'finished with failure'
    JOB_KILLED = 'job killed'
    WORKER_FAILURE = 'worker failure'


class JobSchema(colander.MappingSchema):
    job_id = SchemaNode(colander.Int())
    user = SchemaNode(colander.String())
    cwd = SchemaNode(colander.String())
    command = SchemaNode(colander.String())
    environment = colander.MappingSchema()

