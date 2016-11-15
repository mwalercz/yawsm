import logging
import ssl
import sys

import asyncio
import os
from ws_dist_queue.message import WorkMessage, ListWorkMessage, KillWorkMessage
from ws_dist_queue.message_sender import MessageSender, JsonDeserializer, JsonSerializer
from ws_dist_queue.user.cookie_keeper import CookieKeeper
from ws_dist_queue.user.factory import UserFactory
from ws_dist_queue.user.input_parser import InputParser
from ws_dist_queue.user.protocol import UserProtocol


class UserApp:
    def __init__(self, conf, credentials, message):
        self.conf = conf
        self.loop = asyncio.get_event_loop()
        self.init_logging()
        self.factory = self.init_factory(
            credentials=credentials,
            message=message,
        )

    def run(self):
        coro = self.loop.create_connection(
            protocol_factory=self.factory,
            host=self.conf.MASTER_HOST,
            port=self.conf.MASTER_WSS_PORT,
            ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
        )
        self.loop.run_until_complete(coro)
        self.loop.run_forever()
        self.loop.close()

    def init_factory(self, credentials, message):
        factory = UserFactory(
            conf=self.conf,
            credentials=credentials,
            message=message,
            **self.init_services(),
        )
        factory.protocol = UserProtocol
        return factory

    def init_logging(self):
        self.loop.set_debug(True)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(name)s  %(message)s')

    def init_services(self):
        message_sender = MessageSender(
            message_from='user'
        )
        cookie_keeper = CookieKeeper(self.conf)
        services = {
            'message_sender': message_sender,
            'deserializer': JsonDeserializer(),
            'serializer': JsonSerializer(),
            'cookie_keeper': cookie_keeper,
            'loop': self.loop,
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
        if hasattr(args, 'command'):
            return WorkMessage(
                command=args.command,
                cwd=os.getcwd()
            )
        elif hasattr(args, 'list'):
            return ListWorkMessage()
        elif hasattr(args, 'kill_work_id'):
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