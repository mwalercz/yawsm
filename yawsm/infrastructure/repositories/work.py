from typing import List

from peewee_async import Manager

import yawsm
from yawsm.exceptions import WorkNotFound
from yawsm.infrastructure.db.work import Work, WorkEvent
from yawsm.work.model import WorkStatus
from yawsm.work.actions.dtos import NewWorkDto


class WorkSaver:
    def __init__(self, objects: Manager):
        self.objects = objects

    async def save(self, work: NewWorkDto, user_id: int) -> Work:
        created_work = await self.objects.create(
            Work,
            command=work.command,
            cwd=work.cwd,
            env=work.env,
            status=WorkStatus.new.name,
            user_id=user_id,
        )
        await self.objects.create(
            WorkEvent,
            work_id=created_work.work_id,
            status=WorkStatus.new.name,
            event_type='work_created',
        )
        return created_work


class WorkEventSaver:
    def __init__(self, objects: Manager):
        self.objects = objects

    async def save_event(self, work_event: yawsm.work.model.WorkEvent):
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
            event_type=work_event.reason,
        )


class WorkFinder:
    def __init__(self, objects: Manager):
        self.objects = objects

    async def find_by_work_id_and_user_id(
            self, work_id, user_id
    ) -> Work:
        query = Work.select().where(
            Work.work_id == work_id,
            Work.user_id == user_id,
        ).limit(1)

        result = await self.objects.execute(query)
        try:
            return list(result)[0]
        except IndexError:
            raise WorkNotFound(work_id=work_id, user_id=user_id)

    async def find_by_work_id_and_user_id_with_events(
            self, work_id: int, user_id: int
    ) -> Work:
        query = Work.select(Work, WorkEvent).join(
            WorkEvent
        ).where(
            Work.work_id == work_id,
            Work.user_id == user_id,
        ).limit(1)

        result = await self.objects.execute(query)
        try:
            return list(result)[0]
        except IndexError:
            raise WorkNotFound(work_id=work_id, user_id=user_id)

    async def find_by_user_id(self, user_id: int) -> List[Work]:
        query = Work.select().where(
            Work.user_id == user_id,
        )
        result = await self.objects.execute(query)
        try:
            list(result)[0]
        except IndexError:
            return []
        return result

    async def find_by_statuses(self, statuses: List[str]) -> List[Work]:
        query = Work.select().where(
            Work.status << statuses
        )
        return await self.objects.execute(query)

