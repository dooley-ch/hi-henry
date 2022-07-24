# *******************************************************************************************
#  File:  mysql_explorer_test.py
#
#  Created: 19-07-2022
#
#  History:
#  19-07-2022: Initial version
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

import pytest
import hi_henry.src.plugin as plugin
import hi_henry.src.model as model
import hi_henry.src.errors as errors


class TestMySQLExplorer:
    def test_database(self, mysql_connection: model.IConnection) -> None:
        explorer = plugin.MySQLDatabaseExplorer()
        schema = explorer.extract(mysql_connection)

        assert schema
        assert schema.name == "mistral"
        assert schema.type == model.DatabaseType.MySQL
        assert len(schema.views) == 2
        assert len(schema.tables) == 27

    def test_views(self, mysql_connection: model.IConnection) -> None:
        explorer = plugin.MySQLDatabaseExplorer()
        schema = explorer.extract(mysql_connection)

        assert len(schema.views) == 2
        assert 'albums' in schema.views
        assert 'playlists' in schema.views

        view: model.View = schema.views['albums']
        assert len(view.columns) == 3
        assert 'id' in view.columns
        assert 'title' in view.columns
        assert 'artist' in view.columns

        view = schema.views['playlists']
        assert len(view.columns) == 3

    def test_invalid_database(self, invalid_mysql_connection: model.IConnection) -> None:
        explorer = plugin.MySQLDatabaseExplorer()

        with pytest.raises(errors.DatabaseNotFoundError) as e:
            explorer.extract(invalid_mysql_connection)

        assert 'The following database could not be found' in str(e)

    def test_tables(self, mysql_connection: model.IConnection) -> None:
        explorer = plugin.MySQLDatabaseExplorer()
        schema = explorer.extract(mysql_connection)

        assert len(schema.tables) == 27
        assert 'album' in schema.tables
        assert 'artist' in schema.tables


class TestMySQLExplorerTable:
    def test_columns(self, mysql_connection: model.IConnection):
        explorer = plugin.MySQLDatabaseExplorer()
        schema = explorer.extract(mysql_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Columns
        assert len(album.columns) == 7

        # Primary key
        assert 'id' in album.columns
        col = album.columns['id']
        assert col.is_primary
        assert col.is_auto
        assert col.data_type == 'int'

        # Title
        assert 'title' in album.columns
        col = album.columns['title']
        assert not col.is_primary
        assert col.data_type == 'varchar'

        # Created At
        assert 'created_at' in album.columns
        col = album.columns['created_at']
        assert col.default == 'CURRENT_TIMESTAMP'

    def test_foreign_keys(self, mysql_connection: model.IConnection):
        explorer = plugin.MySQLDatabaseExplorer()
        schema = explorer.extract(mysql_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Foreign keys
        assert len(album.foreign_keys) == 1

        fk = album.foreign_keys[0]

        assert fk.foreign_table == 'artist'
        assert fk.foreign_column == 'id'
        assert fk.column == 'artist_id'

    def test_indexes(self, mysql_connection: model.IConnection) -> None:
        explorer = plugin.MySQLDatabaseExplorer()
        schema = explorer.extract(mysql_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Indexes
        assert len(album.indexes) == 3
        index = album.indexes[1]

        assert index.name == 'artist_album'
        assert not index.is_unique
