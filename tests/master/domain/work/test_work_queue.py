from collections import OrderedDict

import pytest

from ws_dist_queue.master.domain.exceptions import WorkNotFound
from ws_dist_queue.master.domain.work.model import Work
from ws_dist_queue.master.domain.work.work_queue import WorkQueue


class TestWorkQueue:
    @pytest.fixture
    def fixt_work_queue(self):
        return WorkQueue(OrderedDict())

    def test_when_nothing_added_queue_should_be_empty(
            self, fixt_work_queue,
    ):
        assert fixt_work_queue.empty is True

    def test_when_one_element_added_queue_should_not_be_empty(
            self, fixt_work_queue, fixt_work
    ):
        fixt_work_queue.put(fixt_work)
        assert fixt_work_queue.empty is False

    def test_when_one_element_added_it_should_be_found(
            self, fixt_work_queue, fixt_work
    ):
        with pytest.raises(WorkNotFound):
            fixt_work_queue.pop_by_id(fixt_work.work_id)

        fixt_work_queue.put(fixt_work)

        assert fixt_work == fixt_work_queue.pop_by_id(fixt_work.work_id)
        with pytest.raises(WorkNotFound):
            fixt_work_queue.pop_by_id(fixt_work.work_id)

    def test_when_one_element_added_it_should_be_popped(
            self, fixt_work_queue, fixt_work
    ):
        fixt_work_queue.put(fixt_work)
        assert fixt_work == fixt_work_queue.pop()

    def test_when_two_elements_added_first_they_should_be_popped_in_fifo(
            self, fixt_work_queue, fixt_command_data, fixt_credentials
    ):
        work_1 = Work.new(fixt_command_data, fixt_credentials)
        work_2 = Work.new(fixt_command_data, fixt_credentials)

        fixt_work_queue.put(work_1)
        fixt_work_queue.put(work_2)

        assert work_1 == fixt_work_queue.pop()
        assert work_2 == fixt_work_queue.pop()