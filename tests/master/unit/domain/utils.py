from unittest.mock import call, sentinel

import dateutil.parser as parser


def parse_to_datetime(date_text):
    return parser.parse(date_text)


def assert_work_is_ready_sent_to_2_workers(mock_worker_client):
    mock_worker_client.send.assert_has_calls([
        call(recipient=sentinel.worker_ref_1,
             action_name='work_is_ready'),
        call(recipient=sentinel.worker_ref_2,
             action_name='work_is_ready')
    ])
