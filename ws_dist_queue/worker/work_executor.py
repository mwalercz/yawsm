import paramiko


class WorkExecutor:
    INVOKE_BASH = r"bash -c"
    ECHO_PID = r"echo $$"
    GOTO_DIR = r"cd {}"
    EXEC_CMD = r"exec {}"

    def __init__(self, work):
        self.work = work
        self.pid = None

    def do_work(self):
        ssh = self.login_as_user()
        cmd_to_exec = self.EXEC_CMD.format(self.work.command)
        goto_dir = self.GOTO_DIR.format(self.work.cwd)
        command = r"{invoke_bash} '{echo_pid}; {exec_cmd}'".format(
            invoke_bash=self.INVOKE_BASH,
            echo_pid=self.ECHO_PID,
            goto_dir=goto_dir,
            exec_cmd=cmd_to_exec,
        )
        self.pid, channel = self.exec_command(ssh, command)
        return channel.recv_exit_status()

    def kill_work(self):
        if self.pid:
            ssh = self.login_as_user()
            kill_command = r"kill -9 {pid}".format(pid=self.pid)
            command = r"{invoke_bash} '{echo_pid}; {exec_command}'".format(
                invoke_bash=self.INVOKE_BASH,
                echo_pid=self.ECHO_PID,
                exec_command=kill_command
            )
            self.pid, channel = self.exec_command(ssh, command)
            return channel.recv_exit_status()

    def login_as_user(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('localhost', username=self.work.username, password=self.work.password)
        return ssh

    def exec_command(self, ssh, command):
        stdin, stdout, stderr = ssh.exec_command(command)
        return int(stdout.readline()), stdout.channel