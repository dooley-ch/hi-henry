# *******************************************************************************************
#  File:  config.py
#
#  Created: 17-07-2022
#
#  History:
#  17-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['database_file_name', 'activity_log_file_name', 'core_log_file_name', 'error_log_file_name']

from pathlib import Path
import click


def _app_folder() -> Path:
    """
    This function returns the application support folder
    """
    return Path(click.get_app_dir('hi-henry'))


def database_file_name() -> Path:
    """
    This function returns the name of the database file
    """
    return _app_folder().joinpath('projects.json')


def activity_log_file_name() -> Path:
    """
    This function returns the name of the active log file
    """
    return _app_folder().joinpath('activity.log')


def core_log_file_name() -> Path:
    """
    This function returns the name of the core log file
    """
    return _app_folder().joinpath('core.log')


def error_log_file_name() -> Path:
    """
    This function returns the name of the error log file
    """
    return _app_folder().joinpath('error.log')


def map_file_name() -> Path:
    """
    This function returns the name of the error log file
    """
    return _app_folder().joinpath('map.cfg')
