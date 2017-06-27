import logging

from ws_dist_queue.master.domain.exceptions import InvalidStateException

log = logging.getLogger(__name__)


class Worker:
    def __init__(self, worker_id, worker_ref, current_work=None):
        self.worker_id = worker_id
        self.worker_ref = worker_ref
        self.current_work = current_work

    def has_work(self):
        return bool(self.current_work)

    def assign(self, work):
        if self.current_work is None:
            self.current_work = work
        else:
            raise InvalidStateException(
                'Work: {work_id} was assigned to worker: {worker_id}, '
                'which already had work: {current_work_id}'.format(
                    work_id=work.work_id,
                    worker_id=self.worker_id,
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
                'Worker: {worker_id} was removed, '
                'but he wasnt executing job'.format(
                    worker_id=self.worker_id))
            return
        not_finished_work = self.current_work
        self.current_work = None
        log.info(
            'Worker: {worker_id} has died '
            'while working on: {work}'.format(
                worker_id=self.worker_id, work=not_finished_work))
        return not_finished_work

