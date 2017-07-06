from dq_broker.infrastructure.controllers.default import DefaultController


def default_controller(c):
    return DefaultController(
        router=c('router')
    )


def register(c):
    c.add_service(default_controller, 'controllers.default')