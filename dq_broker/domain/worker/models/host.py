from collections import deque
from typing import Deque


class Host:
    DEFAULT_SYSTEM_STATS_SIZE = 10

    def __init__(
            self,
            host_address: str,
            cpu_count: int,
            total_memory: int,
            max_system_stats_size: int = None,
    ):
        self.total_memory = total_memory
        self.cpu_count = cpu_count
        self.system_stats: Deque[SystemStat] = deque(
            maxlen=max_system_stats_size or self.DEFAULT_SYSTEM_STATS_SIZE
        )
        self.host_address = host_address

    def add_system_stat(self, system_stat):
        self.system_stats.appendleft(system_stat)

    def calculate_avg_available_load(self):
        size = len(self.system_stats)
        if size == 0:
            return 0
        total_available_load = 0
        for stat in self.system_stats:
            available_load = self.cpu_count - stat.cpu.load_15
            total_available_load += available_load

        avg_available_load = total_available_load / size
        return avg_available_load
