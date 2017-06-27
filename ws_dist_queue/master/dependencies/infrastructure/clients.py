from ws_dist_queue.master.infrastructure.clients import UserClient, WorkerClient


def user_client(c):
    return UserClient(c('serializer'))


def worker_client(c):
    return WorkerClient(c('serializer'))


def register(c):
    c.add_service(user_client)
    c.add_service(worker_client)
