# *******************************************************************************************
#  File:  data_maps.py
#
#  Created: 24-07-2022
#
#  History:
#  24-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['load_config']

import pathlib
import tomli
from .model import DataTypeMap


def load_config(file: pathlib.Path) -> list[DataTypeMap]:
    """
    This function loads the maps from the original data file
    """
    with file.open('rb') as f:
        data = tomli.load(f)

    maps = list()

    for item in data['maps']:
        name = item['name']
        from_type = item['from_type']
        to_type = item['to_type']
        default = item['default_type']

        rec = DataTypeMap(name, from_type,to_type, default)

        for key, value in item.items():
            if key in ['name', 'from_type','to_type', 'default_type']:
                continue
            rec.map[key] = value

        maps.append(rec)

    return maps
