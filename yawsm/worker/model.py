import datetime
import logging

from collections import deque
from schematics import Model
from schematics.types import IntType, DateTimeType, FloatType

from yawsm.exceptions import InvalidStateException
from yawsm.work.model import Work

log = logging.getLogger(__name__)


class SystemStat(Model):
    load_15 = FloatType(required=True)
    available_memory = IntType(required=True)
    created_at = DateTimeType(default=datetime.datetime.now)


class Host:
    DEFAULT_SYSTEM_STATS_SIZE = 10

    def __init__(
            self,
            host_address: str,
            cpu_count: int,
            total_memory: int,
            max_system_stats_size: int = None,
    ):
        self.total_memory = total_memory
        self.cpu_count = cpu_count
        self.system_stats = deque(
            maxlen=max_system_stats_size or self.DEFAULT_SYSTEM_STATS_SIZE
        )
        self.host_address = host_address

    @property
    def last_system_stat(self):
        try:
            return self.system_stats[0]
        except KeyError:
            return None

    def add_system_stat(self, system_stat: SystemStat):
        self.system_stats.appendleft(system_stat)

    @property
    def avg_available_load(self):
        return self.cpu_count - self.avg_load

    @property
    def avg_available_memory(self):
        size = len(self.system_stats)
        if size == 0:
            return 0.0
        total_available_memory = 0
        for stat in self.system_stats:
            total_available_memory += stat.available_memory

        avg_available_memory = total_available_memory / size
        return avg_available_memory

    @property
    def avg_load(self):
        size = len(self.system_stats)
        if size == 0:
            return 0.0
        total_load = 0.0
        for stat in self.system_stats:
            total_load += stat.load_15

        avg_load = total_load / size
        return avg_load


class Worker:
    def __init__(
            self,
            host,
            worker_socket,
            worker_ref,
            current_work=None
    ):
        self.host: Host = host
        self.worker_socket = worker_socket
        self.worker_ref = worker_ref
        self.current_work: Work = current_work

    def has_work(self):
        return bool(self.current_work)

    def assign(self, work: Work):
        if self.current_work is None:
            self.current_work = work
        else:
            raise InvalidStateException(
                'Assign was called on worker {worker_socket}, which already had work. '
                'New work: {work_id} '
                'Current work: {current_work_id}.'.format(
                    work_id=work.work_id,
                    worker_socket=self.worker_socket,
                    current_work_id=self.current_work.work_id
                ))

    def work_finished(self, work_id):
        if self.current_work is None:
            raise InvalidStateException(
                'Work was finished, but worker didnt have any job assigned')
        if self.current_work.work_id != work_id:
            self.current_work = None
            raise InvalidStateException(
                'Work was finished, but worker was working on something else'
            )
        self.current_work = None

    def remove_work(self):
        if self.current_work is not None:
            current_work = self.current_work
            self.current_work = None
            return current_work

    def remove(self):
        if not self.has_work:
            log.info(
                'Worker: {worker_socket} was removed, '
                'but he wasnt executing job'.format(
                    worker_socket=self.worker_socket))
            return
        not_finished_work = self.current_work
        self.current_work = None
        log.info(
            'Worker: {worker_socket} has died '
            'while working on: {work}'.format(
                worker_socket=self.worker_socket, work=not_finished_work))
        return not_finished_work

    def add_system_stat(self, system_stat: SystemStat):
        self.host.add_system_stat(system_stat)

    @property
    def system_stats(self):
        return self.host.system_stats

    @property
    def last_system_stat(self):
        return self.host.last_system_stat
