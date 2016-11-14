import colander
from colander import SchemaNode


class Work:
    def __init__(
            self, cwd, command, username=None,
            environment=None, work_id=None,
            status=None, password=None
    ):
        self.work_id = work_id
        self.username = username
        self.password = password
        self.cwd = cwd
        self.command = command
        self.environment = environment or {}
        self.status = status


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

