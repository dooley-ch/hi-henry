# *******************************************************************************************
#  File:  system_config.py
#
#  Created: 13-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  13-04-2022: Initial version
#
# *******************************************************************************************

"""
This module provides access to the system parameters
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['get_explorer_plugins', 'get_generator_plugins', 'PluginInfo', 'configure_logging']

import pydantic
import tomli
from pathlib import Path
from typing import List, Dict, Union, Optional
from logging.config import dictConfig
import archive.core.utils as utils


class PluginInfo(pydantic.BaseModel):
    """
    This class represents the definition of a database explorer plugin in the system config file
    """
    name: str
    file: str


def _load_config() -> Dict[str, List]:
    """
    This function loads the data contained in the system.toml
    """
    file: Path = utils.get_config_folder().joinpath('system.toml')

    with open(file, "rb") as f:
        return tomli.load(f)


def get_explorer_plugins() -> Union[List[PluginInfo], None]:
    """
    This function returns the plugin definitions from the system.toml file
    """
    content = _load_config()

    if 'explorer_plugins' in content.keys():
        plugins: Dict = content['explorer_plugins']
        return [PluginInfo(**item) for _, item in plugins.items()]


def get_generator_plugins() -> Union[List[PluginInfo], None]:
    """
    This function returns the plugin definitions from the system.toml file
    """
    content = _load_config()

    if 'explorer_plugins' in content.keys():
        plugins: Dict = content['generator_plugins']
        return [PluginInfo(**item) for _, item in plugins.items()]


def get_data_map(driver: str) -> Dict[str, str] | None:
    """
    This function returns a data map definition from the system.toml file
    """
    content = _load_config()

    key: str = f"datamap_{driver}"

    if key in content.keys():
        data_map = content[key]
        return data_map


def configure_logging(logging_folder: Optional[Path | None] = None) -> None:
    """
    This function configures application logging
    """
    if logging_folder is None:
        logging_folder = utils.get_logs_folder()

    main_file: Path = logging_folder.joinpath('core.log')
    activity_file: Path = logging_folder.joinpath('activity.log')
    error_file: Path = logging_folder.joinpath('error.log')

    config_file: Path = utils.get_config_folder().joinpath('logging.toml')
    with config_file.open('rb') as file:
        config_data = tomli.load(file)

    config_data['handlers']['file_handler']['filename'] = main_file
    config_data['handlers']['error_file_handler']['filename'] = error_file
    config_data['handlers']['progress_file_handler']['filename'] = activity_file

    dictConfig(config_data)
