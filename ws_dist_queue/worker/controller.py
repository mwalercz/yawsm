from twisted.internet import threads
from ws_dist_queue.message import WorkerRequestsWorkMessage, WorkIsDoneMessage, WorkWasKilledMessage
from ws_dist_queue.worker.work_executor import WorkExecutor


class WorkerController:
    def __init__(self, message_sender):
        self.message_sender = message_sender
        self.work_executor = None
        self.current_work = None
        self.master = None  # will be injected later

    def work_is_ready(self, message):
        if self.current_work:
            pass
        else:
            self.message_sender.send(
                self.master,
                WorkerRequestsWorkMessage()
            )

    def no_work_to_be_done(self, message):
        if self.current_work:
            pass
        else:
            pass

    def work_to_be_done(self, message):
        if self.current_work:
            pass
        else:
            self.work_executor = WorkExecutor(work=message.work)
            self.current_work = threads.deferToThread(
                self.work_executor.do_work,
            )
            self.current_work.addCallback(self.work_completed)

    def kill_work(self, message):
        if self.current_work:
            future = threads.deferToThread(
                self.work_executor.kill_work,
            )
            self.current_work.callbacks = []
            future.addCallback(self.work_was_killed)

    def work_was_killed(self, result):
        print('work was killed: ' + str(result))
        self.message_sender.send(
            self.master,
            WorkWasKilledMessage()
        )
        self.current_work = None
        self.message_sender.send(
            self.master,
            WorkerRequestsWorkMessage(),
        )

    def work_completed(self, message):
        self.message_sender.send(
            self.master,
            WorkIsDoneMessage(),
        )
        self.current_work = None
        self.message_sender.send(
            self.master,
            WorkerRequestsWorkMessage()
        )

    def clean_up(self):
        if self.current_work:
            threads.deferToThread(
                self.work_executor.kill_work,
            )
            self.current_work.callbacks = []
