from ws_dist_queue.master.infrastructure.services.clients import ResponseClient, WorkerClient


def response_client(c):
    return ResponseClient(c('serializer'))


def worker_client(c):
    return WorkerClient(c('serializer'))


def register(c):
    c.add_service(response_client)
    c.add_service(worker_client)
