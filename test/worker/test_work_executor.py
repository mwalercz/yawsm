from ws_dist_queue.model.work import Work
from ws_dist_queue.worker.work_executor import WorkExecutor


class TestWorkExecutor:
    def test_work_should_be_done(self):
        work = Work(
            cwd='/home/mwal',
            command='ls',
            username='test',
            password='test123'
        )
        work_executor = WorkExecutor(work=work)
        result = work_executor.do_work()
        assert result == 0
        assert work_executor.pid is not None and isinstance(work_executor.pid, int)

    def test_work_should_fail(self):
        work = Work(
            cwd='/home/mwal',
            command='uhuh',
            username='test',
            password='test123'
        )
        work_executor = WorkExecutor(work=work)
        result = work_executor.do_work()
        assert result != 0

    def test_work_should_be_killed(self):
        work = Work(
            cwd='/home/mwal',
            command='sleep 5',
            username='test',
            password='test123'
        )
