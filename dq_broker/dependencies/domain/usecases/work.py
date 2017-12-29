from dq_broker.work.actions.change_status_usecase import ChangeStatusUsecase
from dq_broker.work.actions.details.usecase import WorkDetailsUsecase
from dq_broker.work.actions.kill.usecase import KillWorkUsecase
from dq_broker.work.actions.list.usecase import ListWorkUsecase

from dq_broker.work.actions.new.usecase import NewWorkUsecase


def kill_work_usecase(c):
    return KillWorkUsecase(
        work_queue=c('work_queue'),
        workers=c('workers'),
        event_saver=c('event_saver'),
        work_finder=c('work_finder'),
        worker_client=c('worker_client'),
    )


def list_work_usecase(c):
    return ListWorkUsecase(
        work_finder=c('work_finder')
    )


def new_work_usecase(c):
    return NewWorkUsecase(
        work_queue=c('work_queue'),
        task_queue=c('task_queue'),
        work_saver=c('work_saver')
    )


def work_details_usecase(c):
    return WorkDetailsUsecase(
        work_finder=c('work_finder'),
    )


def change_status_usecase(c):
    return ChangeStatusUsecase(
        work_finder=c('work_finder'),
        work_event_saver=c('event_saver'),
    )


def register(c):
    c.add_service(kill_work_usecase, 'actions.work.kill_work')
    c.add_service(list_work_usecase, 'actions.work.list_work')
    c.add_service(new_work_usecase, 'actions.work.new_work')
    c.add_service(work_details_usecase, 'actions.work.work_details')
    c.add_service(change_status_usecase, 'actions.work.change_status')
