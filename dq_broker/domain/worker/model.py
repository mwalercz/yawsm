import logging

from dq_broker.domain.exceptions import InvalidStateException
from dq_broker.domain.work.model import Work

log = logging.getLogger(__name__)


class Worker:
    def __init__(self, worker_socket, worker_ref, current_work=None):
        self.worker_socket = worker_socket
        self.worker_ref = worker_ref
        self.current_work: Work = current_work
        self.system_stats = []

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

    def append_system_stat(self, system_stat):
        self.system_stats.append(system_stat)

    def get_last_system_stat(self):
        if len(self.system_stats) > 0:
            return self.system_stats[-1]
        else:
            return None
