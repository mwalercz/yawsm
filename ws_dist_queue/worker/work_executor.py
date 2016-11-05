import paramiko


class WorkExecutor:
    PID_HACK = r"bash -c 'echo $$; exec"

    def __init__(self, work):
        self.work = work
        self.pid = None

    def do_work(self):
        ssh = self.login_as_user()
        command = "{} {}'".format(self.PID_HACK, self.work.command)
        self.pid, channel = self.exec_command(ssh, command)
        return channel.recv_exit_status()

    def kill_work(self):
        if self.pid:
            ssh = self.login_as_user()
            kill_command = "kill -9 {}".format(str(self.pid))
            command = "{} {}'".format(self.PID_HACK, kill_command)
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