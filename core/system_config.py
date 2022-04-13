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

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['get_plugins', 'PluginInfo']

import pydantic
import tomli
from pathlib import Path
from typing import List, Dict

import core.utils as utils


class PluginInfo(pydantic.BaseModel):
    driver: str
    file: str


def _load_config() -> Dict[str, List]:
    file: Path = utils.get_config_folder().joinpath('system.toml')

    with open(file, "rb") as f:
        return tomli.load(f)


def get_plugins() -> List[PluginInfo] | None:
    content = _load_config()

    if 'plugins' in content.keys():
        plugins = content['plugins']
        return [PluginInfo(**item) for item in plugins]
