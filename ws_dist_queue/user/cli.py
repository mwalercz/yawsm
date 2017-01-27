import getpass

import click
import os
import sys
from click import pass_context
from click import prompt
from ws_dist_queue.user.components.authorization import NoCookieException

from ws_dist_queue.user.user_app import make_app


@click.group()
@click.option(
    '-c', '--config',
    default=os.getenv("HOME") + '/.dist_queue/develop.ini',
    type=click.Path(exists=True),
    help='Config path',
    show_default=True
)
@click.option(
    '-l', '--login',
    is_flag=True
)
@pass_context
def queue(ctx, config, login):
    if login:
        username = getpass.getuser()
        password = prompt(text='Password', hide_input=True)
    else:
        username = None
        password = None
    try:
        ctx.obj = make_app(
            config_path=config,
            username=username,
            password=password,
        )
    except NoCookieException:
        username = getpass.getuser()
        password = prompt(text='Password', hide_input=True)
        ctx.obj = make_app(
            config_path=config,
            username=username,
            password=password,
        )
    except Exception as e:
        click.echo('ERROR(s): ' + str(e))
        sys.exit()


@click.argument('command')
@queue.command()
@pass_context
def work(ctx, command):
    app = ctx.obj
    app.send_and_wait(
        path='user/new_work',
        body={
            'command': command,
            'cwd': os.getcwd()
        }
    )


@click.argument('work_id')
@queue.command()
@pass_context
def kill(ctx, work_id):
    app = ctx.obj
    app.send_and_wait(
        path='user/kill_work',
        body={
            'work_id': work_id,
        }
    )


@queue.command()
@pass_context
def ls(ctx):
    app = ctx.obj
    app.send_and_wait(
        path='user/list_work'
    )
