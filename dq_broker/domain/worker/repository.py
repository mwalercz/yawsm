from typing import Dict

from peewee_async import Manager

from dq_broker.infrastructure.db.worker import Host, Worker, SystemStat


class WorkersRepository:
    def __init__(self, objects: Manager):
        self.objects = objects

    async def get_or_create_host(self, host_address):
        obj, created = await self.objects.get_or_create(
            Host,
            defaults={
                'host_address': host_address
            },
            host_address=host_address,
        )
        return obj

    async def create_worker(self, worker_socket, host):
        saved_worker = await self.objects.create(
            Worker,
            worker_socket=worker_socket,
            host=host
        )
        return saved_worker.worker_id

    async def get_system_stats(self, start, worker_ids) -> Dict[int, SystemStat]:
        query = Worker.select(Worker, Host, SystemStat).join(
            Host
        ).join(
            SystemStat
        ).where(
            Worker.worker_id << worker_ids,
            SystemStat.created_at > start
        )
        result = await self.objects.execute(query)
