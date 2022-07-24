# *******************************************************************************************
#  File:  postgresql_explorer_test.py
#
#  Created: 21-07-2022
#
#  History:
#  21-07-2022: Initial version
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


class TestPostgreSqlExplorer:
    def test_database(self, postgresql_connection: model.IConnection) -> None:
        explorer = plugin.PostgreSqlDatabaseExplorer()
        schema = explorer.extract(postgresql_connection)

        assert schema
        assert schema.name == "mistral"
        assert schema.type == model.DatabaseType.PostgreSQL
        assert len(schema.views) == 2
        assert len(schema.tables) == 27

    def test_invalid_database(self, invalid_postgresql_connection: model.IConnection) -> None:
        explorer = plugin.PostgreSqlDatabaseExplorer()

        with pytest.raises(errors.DatabaseNotFoundError) as e:
            explorer.extract(invalid_postgresql_connection)

        assert 'The following database could not be found' in str(e)

    def test_views(self, postgresql_connection: model.IConnection) -> None:
        explorer = plugin.PostgreSqlDatabaseExplorer()
        schema = explorer.extract(postgresql_connection)

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

    def test_tables(self, postgresql_connection: model.IConnection) -> None:
        explorer = plugin.PostgreSqlDatabaseExplorer()
        schema = explorer.extract(postgresql_connection)

        assert len(schema.tables) == 27
        assert 'album' in schema.tables
        assert 'artist' in schema.tables


class TestPostgreSqlExplorerTable:
    def test_columns(self, postgresql_connection: model.IConnection):
        explorer = plugin.PostgreSqlDatabaseExplorer()
        schema = explorer.extract(postgresql_connection)

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
        assert col.data_type == 'integer'

        # Title
        assert 'title' in album.columns
        col = album.columns['title']
        assert not col.is_primary
        assert col.data_type == 'character varying'

        # Created At
        assert 'created_at' in album.columns
        col = album.columns['created_at']
        assert col.default == 'CURRENT_TIMESTAMP'

    def test_foreign_keys(self, postgresql_connection: model.IConnection):
        explorer = plugin.PostgreSqlDatabaseExplorer()
        schema = explorer.extract(postgresql_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Foreign keys
        assert len(album.foreign_keys) == 1

        fk = album.foreign_keys[0]

        assert fk.foreign_table == 'artist'
        assert fk.foreign_column == 'id'
        assert fk.column == 'artist_id'

    def test_indexes(self, postgresql_connection: model.IConnection) -> None:
        explorer = plugin.PostgreSqlDatabaseExplorer()
        schema = explorer.extract(postgresql_connection)

        # Table
        assert 'album' in schema.tables
        album = schema.tables['album']

        # Indexes
        assert len(album.indexes) == 1
        index = album.indexes[0]

        assert index.name == 'album_pkey'
        assert index.is_unique
