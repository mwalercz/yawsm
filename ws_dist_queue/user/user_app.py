import sys

import os
from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor
from twisted.python import log
from ws_dist_queue.master.message_sender import MessageSender, JsonDeserializer
from ws_dist_queue.message import WorkMessage, ListWorkMessage, KillWorkMessage
from ws_dist_queue.user.cookie_keeper import CookieKeeper
from ws_dist_queue.user.factory import UserFactory
from ws_dist_queue.user.input_parser import InputParser
from ws_dist_queue.user.protocol import UserProtocol


class UserApp:
    def __init__(self, conf, credentials, message):
        self.init_logging()
        self.factory = self.init_factory(
            conf=conf,
            credentials=credentials,
            message=message,
        )

    def run(self):
        connectWS(self.factory)
        reactor.run()

    def init_factory(self, conf, credentials, message):
        factory = UserFactory(
            conf=conf,
            credentials=credentials,
            message=message,
            **self.init_services(conf),
        )
        factory.protocol = UserProtocol
        return factory

    def init_logging(self):
        log.startLogging(sys.stdout)

    def init_services(self, conf):
        message_sender = MessageSender(
            message_from='user'
        )
        cookie_keeper = CookieKeeper(conf)
        services = {
            'message_sender': message_sender,
            'deserializer': JsonDeserializer(),
            'cookie_keeper': cookie_keeper,
        }
        return services


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def create(cls, username, password):
        if username and password:
            return Credentials(username, password)
        else:
            return None


class MessageFactory:
    def create(self, args):
        if args.command:
            return WorkMessage(
                command=args.command,
                cwd=os.getcwd()
            )
        elif args.list:
            return ListWorkMessage()
        elif args.kill_work_id:
            return KillWorkMessage(
                work_id=args.kill_work_id
            )

if __name__ == "__main__":
    parser = InputParser()
    args = parser.parse()
    credentials = Credentials.create(args.username, args.password)
    message = MessageFactory().create(args)

    import ws_dist_queue.settings.defaults as defaults
    app = UserApp(
        conf=defaults,
        credentials=credentials,
        message=message,
    )
    app.run()