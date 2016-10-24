import colander
from colander import SchemaNode


class Job:
    def __init__(
            self, cwd, command, user=None,
            environment=None, job_id=None,
            status=None, worker=None,
    ):
        self.job_id = job_id
        self.user = user
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
        return Job(
            job_id=job.get('job_id'),
            user=job.get('user'),
            cwd=job.get('cwd'),
            command=job.get('command'),
            environment=job.get('environment')
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

