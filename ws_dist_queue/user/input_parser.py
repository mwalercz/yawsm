import argparse


class InputParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Message to be sent')
        self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument('-u', '--username', default=None)
        self.parser.add_argument('-p', '--password', default=None)
        subparsers = self.parser.add_subparsers(help='commands')

        work_parser = subparsers.add_parser('work', help='Create new work')
        work_parser.add_argument('command', action='store', help='Command to be executed', default=None)

        list_parser = subparsers.add_parser('list', help='List all work')
        list_parser.add_argument('list', action='store_true', default=None)

        kill_parser = subparsers.add_parser('kill', help='Kill work with given id')
        kill_parser.add_argument('kill_work_id', type=int, help='Work id that should be killed', default=None)

    def parse(self):
        return self.parser.parse_args()
