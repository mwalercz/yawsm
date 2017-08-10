from typing import List

from peewee_async import Manager

import dq_broker
from dq_broker.domain.exceptions import WorkNotFound
from dq_broker.domain.work.model import WorkStatus

from dq_broker.infrastructure.db.work import Work, WorkEvent


class WorkSaver:
    def __init__(self, objects: Manager):
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
    def __init__(self, objects: Manager):
        self.objects = objects

    async def save_event(self, work_event: dq_broker.domain.work.model.WorkEvent):
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
    def __init__(self, objects: Manager):
        self.objects = objects

    async def find_by_work_id_and_username(
            self, work_id, username
    ) -> List[Work]:
        query = Work.select().where(
            Work.work_id == work_id,
            Work.username == username,
        ).limit(1)

        result = await self.objects.execute(query)
        try:
            return list(result)[0]
        except IndexError:
            raise WorkNotFound(work_id=work_id, username=username)

    async def find_by_work_id_and_username_with_events(
            self, work_id, username
    ) -> Work:
        query = Work.select(Work, WorkEvent).join(
            WorkEvent
        ).where(
            Work.work_id == work_id,
            Work.username == username,
        ).limit(1)

        result = await self.objects.execute(query)
        try:
            return list(result)[0]
        except IndexError:
            raise WorkNotFound(work_id=work_id, username=username)

    async def find_by_username(self, username) -> List[Work]:
        query = Work.select().where(
            Work.username == username
        )
        work_list = await self.objects.execute(query)
        return work_list or []
