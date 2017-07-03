import logging
from traceback import format_exc

from ws_dist_queue.master.exceptions import ValidationError

log = logging.getLogger(__name__)


class Supervisor:
    def __init__(self, executor, response_client):
        self.executor = executor
        self.response_client = response_client

    async def handle_request(self, request, route):
        try:
            response = await self.executor.execute(
                func=route.handler, arg=request
            )
        except ValidationError as exc:
            log.exception('Validation error: %s', exc)
            self.response_client.send(
                recipient=request.sender,
                response=request.get_response(
                    status_code=400,
                    body={'error': exc.data},
                )
            )
            return
        except Exception as exc:
            log.exception('Error while handling request: %s', str(exc))
            self.response_client.send(
                recipient=request.sender,
                response=request.get_response(
                    status_code=500,
                )
            )
            return

        if response:
            log.info('Response sent: %s', str(response))
            self.response_client.send(
                recipient=request.sender,
                response=response,
            )
