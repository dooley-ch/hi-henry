# *******************************************************************************************
#  File:  data_maps_test.py
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

__all__ = []

import hi_henry.src.data_maps as dm


def test_load_config(data_maps_config_file) -> None:
    data = dm.load_config(data_maps_config_file)
    assert len(data) == 4


def test_populate_map_table(data_maps_config_file, database_file_name) -> None:
    dm.populate_map_table(data_maps_config_file, database_file_name)
    assert data_maps_config_file.exists()


def test_type_map() -> None:
    map = dm.TypeMap("SQLite_To_Standard", "SQLite", "Standard", "String")
    map['INTEGER'] = "Integer"
    map['REAL'] = "Float"
    map['TEXT'] = "String"
    map['BLOB'] = "Binary"

    assert map.name == "SQLite_To_Standard"
    assert map.from_type == "SQLite"
    assert map.to_type =="Standard"
    assert map.default == "String"

    assert map['INTEGER'] == "Integer"
    assert map['REAL'] == "Float"
    assert map['TEXT'] == "String"
    assert map['BLOB'] == "Binary"

    assert map['NULL'] == "String"
