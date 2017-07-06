import logging

log = logging.getLogger(__name__)


class DefaultController:
    def __init__(self, router):
        self.router = router

    def handle(self, req):
        log.warning(req)
        available_paths = self.router.get_available_paths(req.peer)
        return req.get_response(
            status_code=404,
            body={
                'error': 'Path does not exist',
                'path': req.message.path,
                'available_paths': available_paths
            }
        )
