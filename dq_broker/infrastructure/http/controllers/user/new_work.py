from aiohttp import web
from aiohttp_session import get_session

from dq_broker.domain.work.model import CommandData
from dq_broker.domain.work.model import Work
from dq_broker.infrastructure.auth.permits import users_must_match
from dq_broker.infrastructure.auth.user import Credentials
from dq_broker.infrastructure.http.controllers.schema import NewWorkSchema
from dq_broker.infrastructure.http.validator import validate


class NewWorkController:
    def __init__(self, usecase):
        self.usecase = usecase

    @users_must_match
    async def handle(self, request):
        data = await request.json()
        session = await get_session(request)
        validated = validate(data, schema=NewWorkSchema)
        new_work = Work.new(
            command_data=CommandData(
                command=validated.command,
                env=validated.env,
                cwd=validated.cwd,
            ),
            credentials=Credentials(
                username=session['user_info']['username'],
                password=session['user_info']['password'],
            )
        )

        work_id = await self.usecase.perform(new_work)

        return web.json_response(
            {'work_id': work_id},
            status=202
        )
