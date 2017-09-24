from dq_broker.domain.worker.models.host import Host


class InMemoryHosts:
    def __init__(self, hosts):
        self.hosts = hosts

    def get_or_create_host(self, host: Host):
        try:
            return self.hosts[host.host_address], False
        except KeyError:
            self.hosts[host.host_address] = host
            return host, True
