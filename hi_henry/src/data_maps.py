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

__all__ = ['load_config', 'populate_map_table', 'TypeMap']

import pathlib
import tomli
from collections import UserDict
from .model import DataTypeMap
from .dbms import MapStore


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


def populate_map_table(source: pathlib.Path, database_file: pathlib.Path) -> None:
    """
    This function populates the app database with the data type maps
    """
    data = load_config(source)
    db = MapStore(database_file)

    for item in data:
        db.insert(item)


class TypeMap(UserDict):
    """
    Holds the mapping between two types
    """
    _name: str
    _from_type: str
    _to_type: str
    _default: str

    def __init__(self, name: str, from_type: str, to_type: str, default: str):
        super().__init__({})
        self._name = name
        self._from_type = from_type
        self._to_type = to_type
        self._default = default
        self.changed = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def from_type(self) -> str:
        return self._from_type

    @property
    def to_type(self) -> str:
        return self._to_type

    @property
    def default(self) -> str:
        return self._default

    def __getitem__(self, item) -> str:
        if item in self.data:
            return self.data[item]
        return self._default
