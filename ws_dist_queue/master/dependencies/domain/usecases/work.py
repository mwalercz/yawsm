from ws_dist_queue.master.domain.work.usecases.kill_work import KillWorkUsecase
from ws_dist_queue.master.domain.work.usecases.list_work import ListWorkUsecase
from ws_dist_queue.master.domain.work.usecases.new_work import NewWorkUsecase


def kill_work_usecase(c):
    return KillWorkUsecase(
        work_queue=c('work_queue'),
        workers_repo=c('repositories.workers'),
        event_saver=c('repositories.work.event_saver'),
        work_finder=c('repositories.work.work_finder'),
        worker_client=c('clients.worker')
    )


def list_work_usecase(c):
    return ListWorkUsecase(
        work_finder=c('repositories.work.work_finder')
    )


def new_work_usecase(c):
    return NewWorkUsecase(
        work_queue=c('work_queue'),
        workers_notifier=c('workers_notifier'),
        work_repo=c('repositories.workers')
    )

def register(c):
    c.add_service(kill_work_usecase, 'usecases.user.kill_work')
    c.add_service(list_work_usecase, 'usecases.user.list_work')
    c.add_service(new_work_usecase, 'usecases.user.new_work')
