from concurrent.futures import ThreadPoolExecutor

from ws_dist_queue.worker.controller import WorkerController


def worker_controller(c):
    return WorkerController(
        thread_pool=ThreadPoolExecutor(max_workers=2),
        master_client=c('master_client'),
        loop=c('loop'),
    )


def register(c):
    c.add_service(worker_controller)