from dq_broker.domain.work.usecases.kill import KillWorkUsecase
from dq_broker.domain.work.usecases.new import NewWorkUsecase
from dq_broker.domain.work.usecases.details import WorkDetailsUsecase
from dq_broker.domain.work.usecases.list import ListWorkUsecase


def kill_work_usecase(c):
    return KillWorkUsecase(
        work_queue=c('work_queue'),
        workers=c('workers'),
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
    c.add_service(kill_work_usecase, 'usecases.work.kill_work')
    c.add_service(list_work_usecase, 'usecases.work.list_work')
    c.add_service(new_work_usecase, 'usecases.work.new_work')
    c.add_service(work_details_usecase, 'usecases.work.work_details')
