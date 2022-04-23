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
__all__ = ['get_explorer_plugins', 'get_generator_plugins', 'PluginInfo']

import pydantic
import tomli
from pathlib import Path
from typing import List, Dict, Union

import core.utils as utils


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
