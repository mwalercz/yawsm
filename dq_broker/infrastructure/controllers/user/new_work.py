from dq_broker.domain.work.model import CommandData
from dq_broker.domain.work.model import Work
from dq_broker.schema import NewWorkSchema

from dq_broker.infrastructure.services.request import validate


class NewWorkController:
    def __init__(self, user_auth, usecase):
        self.user_auth = user_auth
        self.usecase = usecase

    @validate(schema=NewWorkSchema)
    async def handle(self, req):
        new_work = Work.new(
            command_data=CommandData(
                command=req.validated.command,
                env=req.validated.env,
                cwd=req.validated.cwd,
            ),
            credentials=self.user_auth.get_credentials(req.peer)
        )
        work_id = await self.usecase.perform(new_work)
        return req.get_response(
            status_code=202,
            body={'work_id': work_id}
        )
