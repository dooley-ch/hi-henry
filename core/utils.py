# *******************************************************************************************
#  File:  utils.py
#
#  Created: 09-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  09-04-2022: Initial version
#
# *******************************************************************************************

"""
This module provides common functons and classes used by the application
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['get_config_folder', 'get_logs_folder', 'get_output_folder', 'get_config',
           'get_templates_folder']

import pathlib
import pydantic
import core.custom_types as types


class _ConfigFile(pydantic.BaseSettings):
    """
    This class represents the contents of a configuration file
    """
    database: str
    user: str
    password: str
    driver: str = 'mysql'
    host: str = '127.0.0.1'
    port: int = 3306

    @classmethod
    def driver_is_valid(cls, value: str) -> str:
        if value not in ['mysql']:
            raise ValueError(f"{value} is not a valid database driver!")
        return value

    class Config:
        case_sensitive = False
        env_prefix = 'hih_'


def get_config(file: pathlib.Path) -> types.IDbConnInfo:
    """
    This method loads the configuration information from the given file and returns an
    object consistent with the _ConnectionInfo protocol
    :param file: The file containing the configuration information
    :return: An object consistent with the _ConnectionInfo protocol
    """
    return _ConfigFile(_env_file=file, _env_file_encoding='utf-8')


def get_config_folder() -> pathlib.Path:
    """
    This method returns the location of the config folder
    """
    return pathlib.Path(__file__).parent.parent.joinpath('config')


def get_logs_folder() -> pathlib.Path:
    """
    This method returns the location of the logs' folder
    """
    return pathlib.Path(__file__).parent.parent.joinpath('logs')


def get_output_folder() -> pathlib.Path:
    """
    This method returns the location of the logs' folder
    """
    return pathlib.Path(__file__).parent.parent.joinpath('generated')


def get_templates_folder() -> pathlib.Path:
    """
    This method returns the location of the logs' folder
    """
    return pathlib.Path(__file__).parent.parent.joinpath('templates')
