from dq_broker.domain.work.usecases.kill_work import KillWorkUsecase
from dq_broker.domain.work.usecases.new_work import NewWorkUsecase
from dq_broker.domain.work.usecases.work_details import WorkDetailsUsecase
from dq_broker.domain.work.usecases.list_work import ListWorkUsecase


def kill_work_usecase(c):
    return KillWorkUsecase(
        work_queue=c('work_queue'),
        workers_repo=c('workers_repo'),
        event_saver=c('event_saver'),
        work_finder=c('work_finder'),
        worker_client=c('worker_client')
    )


def list_work_usecase(c):
    return ListWorkUsecase(
        work_finder=c('work_finder')
    )


def new_work_usecase(c):
    return NewWorkUsecase(
        work_queue=c('work_queue'),
        workers_notifier=c('workers_notifier'),
        work_saver=c('work_saver')
    )


def work_details_usecase(c):
    return WorkDetailsUsecase(
        work_finder=c('work_finder'),
    )


def register(c):
    c.add_service(kill_work_usecase, 'usecases.user.kill_work')
    c.add_service(list_work_usecase, 'usecases.user.list_work')
    c.add_service(new_work_usecase, 'usecases.user.new_work')
    c.add_service(work_details_usecase, 'usecases.user.work_details')
