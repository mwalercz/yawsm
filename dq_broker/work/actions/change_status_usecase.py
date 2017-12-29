from typing import List

import logging

from dq_broker.work.model import WorkEvent, WorkStatus

log = logging.getLogger(__name__)


class ChangeStatusUsecase:
    def __init__(self, work_finder, work_event_saver):
        self.work_finder = work_finder
        self.work_event_saver = work_event_saver

    async def perform(
            self,
            from_statuses: List[WorkStatus],
            to_status: str,
            reason: str
    ):
        works = await self.work_finder.find_by_statuses(from_statuses)
        events = [
            WorkEvent(
                work_id=work.work_id,
                reason=reason,
                work_status=to_status,
            ) for work in works
        ]
        for event in events:
            log.info(
                'Status will be changed to "%s" for job: %s',
                event.work_status, event.work_id
            )
            await self.work_event_saver.save_event(event)
