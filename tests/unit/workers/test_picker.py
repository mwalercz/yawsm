from unittest.mock import sentinel

import pytest

from yawsm.worker.model import Worker, Host, SystemStat
from yawsm.worker.picker import SystemInfoBasedPicker

pytestmark = pytest.mark.asyncio

async def test_system_info_picker():
    host_1 = Host(
        host_address='126.0.0.1',
        cpu_count=4,
        total_memory=100,
        max_system_stats_size=3,
    )
    host_1.add_system_stat(
        SystemStat(dict(load_15=2, available_memory=20)),
    )
    host_1.add_system_stat(
        SystemStat(dict(load_15=3, available_memory=20))
    )

    host_2 = Host(
        host_address='215.0.0.1',
        cpu_count=4,
        total_memory=100,
        max_system_stats_size=3,
    )
    host_2.add_system_stat(
        SystemStat(dict(load_15=1, available_memory=20)),
    )
    host_2.add_system_stat(
        SystemStat(dict(load_15=2, available_memory=20))
    )
    worker_1 = Worker(
        host=host_1,
        worker_socket='tcp:126.0.0.1',
        worker_ref=sentinel.worker_ref_1,
    )
    worker_2 = Worker(
        host=host_2,
        worker_socket='tcp:215.0.0.1',
        worker_ref=sentinel.worker_ref_2,
    )
    workers = [worker_1, worker_2]

    picker = SystemInfoBasedPicker(delay=0)
    picked = []
    async for worker in picker.pick_best(workers):
        picked.append(worker)

    assert len(picked) == 2
    assert picked[0] == worker_2
    assert picked[1] == worker_1
