# *******************************************************************************************
#  File:  conftest.py
#
#  Created: 30-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  30-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def app_folder() -> Path:
    return Path(__file__).parent.joinpath('app_folder')


@pytest.fixture(scope="session")
def database_file_name(app_folder) -> Path:
    return app_folder.joinpath('projects.json')


@pytest.fixture(scope="session")
def activity_log_file_name(app_folder) -> Path:
    return app_folder.joinpath('activity.log')


@pytest.fixture(scope="session")
def core_log_file_name(app_folder) -> Path:
    return app_folder.joinpath('core.log')


@pytest.fixture(scope="session")
def error_log_file_name(app_folder) -> Path:
    return app_folder.joinpath('error.log')


@pytest.fixture(scope="session")
def map_file_name(app_folder) -> Path:
    return app_folder.joinpath('map.cfg')
