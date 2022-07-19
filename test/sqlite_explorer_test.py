# *******************************************************************************************
#  File:  sqlite_explorer_test.py
#
#  Created: 18-07-2022
#
#  History:
#  18-07-2022: Initial version
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


import hi_henry.src.plugin as plugin
import hi_henry.src.model as model


class TestSQLiteExplorer:
    def test_database(self, sqlite_connection: model.IConnection) -> None:
        explorer = plugin.SQLiteDatabaseExplorer()
        schema = explorer.extract(sqlite_connection)

        assert schema
        assert schema.name == "mistral"
        assert schema.type == model.DatabaseType.SQLite
        assert len(schema.views) == 2
        assert len(schema.tables) == 26

    def test_views(self, sqlite_connection: model.IConnection) -> None:
        explorer = plugin.SQLiteDatabaseExplorer()
        schema = explorer.extract(sqlite_connection)

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

    def test_tables(self, sqlite_connection: model.IConnection) -> None:
        explorer = plugin.SQLiteDatabaseExplorer()
        schema = explorer.extract(sqlite_connection)

        assert len(schema.tables) == 26
        assert 'album' in schema.tables
        assert 'artist' in schema.tables


class TestSQLiteExplorerTable:
    def test_columns(self, sqlite_connection: model.IConnection):
        explorer = plugin.SQLiteDatabaseExplorer()
        schema = explorer.extract(sqlite_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Columns
        assert len(album.columns) == 7

        # Primary key
        assert 'ID' in album.columns
        col = album.columns['ID']
        assert col.is_primary
        assert col.is_auto
        assert col.data_type == 'INTEGER'

        # Title
        assert 'title' in album.columns
        col = album.columns['title']
        assert not col.is_primary
        assert col.data_type == 'TEXT'

        # Created At
        assert 'created_at' in album.columns
        col = album.columns['created_at']
        assert col.default == 'CURRENT_TIMESTAMP'

    def test_foreign_keys(self, sqlite_connection: model.IConnection):
        explorer = plugin.SQLiteDatabaseExplorer()
        schema = explorer.extract(sqlite_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Foreign keys
        assert len(album.foreign_keys) == 1

        fk = album.foreign_keys[0]

        assert fk.foreign_table == 'artist'
        assert fk.foreign_column == 'ID'
        assert fk.column == 'artist_ID'

    def test_indexes(self, sqlite_connection: model.IConnection) -> None:
        explorer = plugin.SQLiteDatabaseExplorer()
        schema = explorer.extract(sqlite_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Indexes
        assert len(album.indexes) == 2
        index = album.indexes[1]

        assert index.name == 'sqlite_autoindex_album_1'
        assert index.is_unique

