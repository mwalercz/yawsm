from typing import List

from ws_dist_queue.master import domain
from ws_dist_queue.master.domain.work.model import WorkStatus
from ws_dist_queue.master.infrastructure.db.work import Work, WorkEvent


class WorkSaver:
    def __init__(self, objects):
        self.objects = objects

    async def save_new(self, work) -> int:
        created_work = await self.objects.create(
            Work,
            command=work.command_data.command,
            cwd=work.command_data.cwd,
            env=work.command_data.env,
            status=WorkStatus.new.name,
            username=work.credentials.username,
        )
        await self.objects.create(
            WorkEvent,
            work_id=created_work.work_id,
            status=WorkStatus.new.name,
            event_type='work_created',
        )
        return created_work.work_id


class WorkEventSaver:
    def __init__(self, objects):
        self.objects = objects

    async def save_event(self, work_event: domain.work.model.WorkEvent) -> None:
        await self.objects.execute(
            Work.update(
                status=work_event.work_status
            ).where(
                Work.work_id == work_event.work_id
            )
        )
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

    async def find_by_work_id_and_username(
            self, work_id, username) -> List[Work]:
        return await self.objects.get(
            Work.select().where(
                Work.work_id == work_id,
                Work.username == username,
            )
        )

    async def find_by_username(self, username) -> List[Work]:
        query = Work.select().where(
            Work.username == username
        ).order_by(
            Work.created_at
        )
        work_list = await self.objects.execute(query)
        return work_list or []

    async def find_by_work_id_with_events(self, work_id) -> Work:
        return await self.objects.get(
            Work.select().join(
                WorkEvent
            ).where(
                Work.work_id == work_id
            ).order_by(
                WorkEvent.created_at.asc()
            )
        )
