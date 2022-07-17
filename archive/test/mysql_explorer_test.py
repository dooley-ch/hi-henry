# *******************************************************************************************
#  File:  mysql_explorer_test.py
#
#  Created: 24-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  24-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import pytest
from archive.core.project_config import ProjectDefinition
from archive import plugin as plugin


@pytest.fixture()
def connection_info():
    name: str
    explorer: str
    generator: str
    host: str
    port: int
    database: str
    user: str
    password: str
    multi_file: bool

    return ProjectDefinition(name='MySQLTest', explorer="MySQLExplorer", generator="MySQLGenerator", host="127.0.0.1",
                             port=3306, database="mistral", user="root", password="root*347", multi_file=False)


def test_schema_extraction_process(connection_info) -> None:
    explorer = plugin.MySQLExplorer()
    assert explorer.extract(connection_info)


def test_tables_exist(connection_info) -> None:
    explorer = plugin.MySQLExplorer()
    schema = explorer.extract(connection_info)

    assert 'album' in schema.tables
    assert 'artist' in schema.tables
    assert 'customer' in schema.tables
    assert 'track' in schema.tables


def test_columns_exist(connection_info) -> None:
    explorer = plugin.MySQLExplorer()
    schema = explorer.extract(connection_info)

    table = schema.tables['album']
    assert 'title' in table.columns
    assert 'artist_id' in table.columns

    table = schema.tables['artist']
    assert 'ID' in table.columns
    assert 'name' in table.columns

    table = schema.tables['customer']
    assert 'first_name' in table.columns
    assert 'state' in table.columns
    assert 'fax' in table.columns

    table = schema.tables['track']
    assert 'bytes' in table.columns
    assert 'unit_price' in table.columns


def test_primary_key_exists(connection_info):
    explorer = plugin.MySQLExplorer()
    schema = explorer.extract(connection_info)

    table = schema.tables['album']
    assert 'ID' in table.primary_key
    assert len(table.primary_key) == 1

    table = schema.tables['artist']
    assert 'ID' in table.primary_key
    assert len(table.primary_key) == 1

    table = schema.tables['customer']
    assert 'ID' in table.primary_key
    assert len(table.primary_key) == 1

    table = schema.tables['track']
    assert 'ID' in table.primary_key
    assert len(table.primary_key) == 1


def test_index_exists(connection_info):
    explorer = plugin.MySQLExplorer()
    schema = explorer.extract(connection_info)

    table = schema.tables['album']
    assert 'Idx_album_artist_id' in table.indexes
    index = table.indexes['Idx_album_artist_id']
    assert 'artist_id' in index.columns

    table = schema.tables['employee']
    assert 'Idx_employee_manager_id' in table.indexes
    index = table.indexes['Idx_employee_manager_id']
    assert 'manager_id' in index.columns


def test_unique_key_exists(connection_info):
    explorer = plugin.MySQLExplorer()
    schema = explorer.extract(connection_info)

    table = schema.tables['album']
    assert 'Uk_album_title' in table.unique_keys
    unique_index = table.unique_keys['Uk_album_title']
    assert 'title_lower' in unique_index.columns

    table = schema.tables['artist']
    assert 'Uk_artist_name' in table.unique_keys
    unique_index = table.unique_keys['Uk_artist_name']
    assert 'name_lower' in unique_index.columns


def test_foreign_key_exists(connection_info):
    explorer = plugin.MySQLExplorer()
    schema = explorer.extract(connection_info)

    table = schema.tables['album']
    assert 'Fk_album_artist' in table.foreign_keys
    fk = table.foreign_keys['Fk_album_artist']

    assert fk.name == 'Fk_album_artist'
    assert fk.column_name == 'artist_id'
    assert fk.foreign_table_name == 'artist'
    assert fk.foreign_column_name == 'ID'

    table = schema.tables['track']
    assert 'Fk_track_album' in table.foreign_keys
    fk = table.foreign_keys['Fk_track_album']

    assert fk.name == 'Fk_track_album'
    assert fk.column_name == 'album_id'
    assert fk.foreign_table_name == 'album'
    assert fk.foreign_column_name == 'ID'
