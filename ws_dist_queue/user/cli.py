import click
import os
from click import pass_context

from ws_dist_queue.user.user_app import make_app


@click.group()
@click.option(
    '-c', '--config',
    default='conf/develop.ini',
    type=click.Path(exists=True),
    help='Config path',
    show_default=True
)
@click.option(
    '-u', '--username',
    # default='mwal',
)
@click.option(
    '-p', '--password',
    # default='matrix'
)
@pass_context
def queue(ctx, config, username, password):
    click.echo(ctx.obj)
    ctx.obj = make_app(
        config_path=config,
        username=username,
        password=password,
    )


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
