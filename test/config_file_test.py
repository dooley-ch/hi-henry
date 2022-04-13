# *******************************************************************************************
#  File:  config_file_test.py
#
#  Created: 10-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  10-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import pytest
from pathlib import Path
from pydantic.error_wrappers import ValidationError
import core.utils as utils


def test_valid_file() -> None:
    """
    This function tests a fully populated and valid file
    """
    file: Path = Path(__file__).parent.joinpath('data', 'full_valid_file.env')
    config: utils.ConnectionInfo = utils.get_config(file)

    assert config.database == 'database_name'
    assert config.user == 'dba_user'
    assert config.password == 'dba_password'
    assert config.driver == 'mysql'
    assert config.host == '127.0.0.1'
    assert config.port == 3306


def test_valid_file_without_defaults() -> None:
    """
    This function tests a file with only required values
    """
    file: Path = Path(__file__).parent.joinpath('data', 'valid_file_without_defaults.env')
    config: utils.ConnectionInfo = utils.get_config(file)

    assert config.database == 'database_name'
    assert config.user == 'dba_user'
    assert config.password == 'dba_password'
    assert config.driver == 'mysql'
    assert config.host == '127.0.0.1'
    assert config.port == 3306


def test_invalid_file() -> None:
    """
    This function tests an invalid file
    """
    file: Path = Path(__file__).parent.joinpath('data', 'invalid_file.env')

    with pytest.raises(ValidationError):
        utils.get_config(file)
