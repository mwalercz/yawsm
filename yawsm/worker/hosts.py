from yawsm.worker.model import Host


class InMemoryHosts:
    def __init__(self):
        self.hosts = {}

    def get_or_create(self, host: Host):
        try:
            return self.hosts[host.host_address], False
        except KeyError:
            self.hosts[host.host_address] = host
            return host, True
