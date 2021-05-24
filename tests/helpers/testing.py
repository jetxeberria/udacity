"""
Helper methods commonly used in testing
"""
import copy
from time import sleep
from logging import getLogger

import pytest
from daslog import initialize_logging, LogConfig, reset_defaults



def _wait_until(is_state, lapsus=0.1, num_retries=20):
    for _ in range(num_retries):
        sleep(lapsus)
        if is_state():
            return


def _log_config(level="DEBUG"):
    cfg = LogConfig(log_level=level)
    reset_defaults()
    return cfg


@pytest.fixture
def daslogger(caplog):
    """ Initializes daslog and ensures standard logging do not get ever increasing handlers """
    logger = getLogger()
    initial_handlers = copy.copy(logger.handlers)
    initialize_logging(_log_config())
    daslog_handlers = [h for h in logger.handlers if h not in initial_handlers]

    yield caplog

    for h in daslog_handlers:
        logger.removeHandler(h)


def _match_record(record, entry):
    for k, v in entry.items():
        if k not in record:
            return False
        if not entry[k] is None and not v in record[k]:
            return False
    return True


def assert_was_logged(caplog, entries):
    """
    Assert that every required entry was written in the log.

    Each entry is defined by a dictionary of field_name, field_value
    If field_value is None, we only check that the field is found
    If field_value is not None, we also check that the field value is the
    same that we find in the log
    """
    for entry in entries:
        assert any([_match_record(r.msg, entry) for r in caplog.records])



def assert_not_was_logged(caplog, *entries):
    """
    Assert that every required entry was not written in the log.

    Each entry is defined by a dictionary of field_name, field_value
    If field_value is None, we only check that the field is found
    If field_value is not None, we also check that the field value is the
    same that we find in the log
    """
    for entry in entries:
        assert not any([_match_record(r.msg, entry) for r in caplog.records])