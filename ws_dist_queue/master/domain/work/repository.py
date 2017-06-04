from ws_dist_queue.master import domain
from ws_dist_queue.master.domain.work.model import WorkStatus
from ws_dist_queue.master.infrastructure.db.work import Work, WorkEvent


class WorkSaver:
    def __init__(self, objects):
        self.objects = objects

    async def save_new(self, work):
        await self.objects.create(
            Work,
            work_id=work.work_id,
            command=work.command_data.command,
            cwd=work.command_data.cwd,
            env=work.command_data.env,
            status=WorkStatus.new.name,
            username=work.credentials.username,
        )
        await self.objects.create(
            WorkEvent,
            work_id=work.work_id,
            status=WorkStatus.new.name,
            event_type='work_created',
        )


class WorkEventSaver:
    def __init__(self, objects):
        self.objects = objects

    async def save_event(self, work_event: domain.work.model.WorkEvent):
        query = Work.update(
            status=work_event.work_status
        ).where(
            Work.work_id == work_event.work_id
        )
        self.objects.execute(query)
        await self.objects.create(
            WorkEvent,
            work_id=work_event.work_id,
            status=work_event.work_status,
            context=work_event.context,
            event_type=work_event.event_type,
        )


class WorkFinder:
    def __init__(self, objects):
        self.objects = objects

    async def find_by_work_id_and_username(self, work_id, username):
        query = Work.select().where(
            Work.work_id == work_id,
            Work.username == username,
        ).order_by(
            Work.created_at
        )
        work_list = await self.objects.execute(query)
        return work_list

    async def find_by_username(self, username) -> Work:
        query = Work.select().where(
            Work.username == username
        ).order_by(
            Work.created_at
        )
        work_list = await self.objects.execute(query)
        return work_list
