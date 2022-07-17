# *******************************************************************************************
#  File:  logging_test.py
#
#  Created: 21-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  21-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import pathlib
import logging
from collections import deque
import pytest
from archive import core as sys_config

_logs = pathlib.Path(__file__).parent.joinpath('test_data')
_error_log: pathlib.Path = _logs.joinpath('error.log')
_activity_log: pathlib.Path = _logs.joinpath('activity.log')
_main_log: pathlib.Path = _logs.joinpath('core.log')


@pytest.fixture
def reset():
    if _main_log.exists():
        _main_log.unlink()
    if _activity_log.exists():
        _activity_log.unlink()
    if _error_log.exists():
        _error_log.unlink()


def get_last_line(file: pathlib.Path):
    with open(file) as f:
        entry: str = deque(f, 10).pop()
        return entry.strip()


def test_file_config(reset):
    sys_config.configure_logging(_logs)

    assert _main_log.exists()
    assert _activity_log.exists()
    assert _error_log.exists()


def test_write_root_info(reset) -> None:
    sys_config.configure_logging(_logs)

    log: logging.Logger = logging.getLogger()
    log.info('Test info message')

    last_entry: str = get_last_line(_main_log)

    assert last_entry.endswith('Test info message')


def test_write_root_error(reset) -> None:
    sys_config.configure_logging(_logs)

    log: logging.Logger = logging.getLogger()
    log.error('Test error message')

    last_entry: str = get_last_line(_main_log)
    assert last_entry.endswith('Test error message')

    last_entry: str = get_last_line(_error_log)
    assert 'Test error message' in last_entry


def test_write_process_logging(reset) -> None:
    sys_config.configure_logging(_logs)

    log: logging.Logger = logging.getLogger('progress_logger')
    log.info('Test info message')

    last_entry: str = get_last_line(_activity_log)
    assert last_entry.endswith('Test info message')

    last_entry: str = get_last_line(_main_log)
    assert last_entry.endswith('Test info message')
