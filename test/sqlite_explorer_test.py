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
