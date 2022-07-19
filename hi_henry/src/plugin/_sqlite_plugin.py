# *******************************************************************************************
#  File:  _sqlite_plugin.py
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
__all__ = ['SQLiteDatabaseExplorer']

import re
import sqlite3

import attrs

from ..model import ViewColumn, View, Column, Index, ForeignKey, Table, Database, IConnection, DatabaseType


# noinspection SqlDialectInspection
class SQLiteDatabaseExplorer:
    """
    This class handles the extraction of the SQLite database schema
    """

    # region Views

    @staticmethod
    def _get_view_names(con: sqlite3.Connection) -> list[str] | None:
        """
        Returns the names of the tables in the database
        """
        cursor = con.cursor()
        rows = cursor.execute("""SELECT name FROM sqlite_schema 
                                    WHERE type ='view' AND name NOT LIKE 'sqlite_%' ORDER BY name;""").fetchall()
        if rows:
            table_names = list()
            for row in rows:
                table_names.append(row['name'])
            return table_names

    @staticmethod
    def _get_view(con: sqlite3.Connection, name: str) -> View:
        """
        This method extracts the view definition
        """
        cursor = con.cursor()
        vw = View(name)

        # Columns
        rows = cursor.execute(f"pragma table_info('{name}');").fetchall()
        if rows:
            for row in rows:
                name = row['name']
                data_type = row['type']
                order = row['cid']

                vw.columns[name] = ViewColumn(name, data_type, order, 0)

        return vw

    # endregion

    # region Tables

    @staticmethod
    def _get_table_names(con: sqlite3.Connection) -> list[str] | None:
        """
        Returns the names of the tables in the database
        """
        cursor = con.cursor()
        rows = cursor.execute("""SELECT name FROM sqlite_schema 
                                    WHERE type ='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;""").fetchall()
        if rows:
            table_names = list()
            for row in rows:
                table_names.append(row['name'])
            return table_names

    @staticmethod
    def _get_table_columns(con: sqlite3.Connection, name: str) -> list[Column]:
        """
        This method extracts the column definitions for a table
        """
        cursor = con.cursor()
        columns = list()

        rows = cursor.execute(f"pragma table_info('{name}');").fetchall()
        if rows:
            for row in rows:
                col_name = row['name']
                data_type = row['type']
                order = row['cid']
                is_null = not bool(row['notnull'])
                default_value = row['dflt_value']
                is_pk = bool(row['pk'])

                columns.append(Column(col_name, data_type, order, 0,
                                      is_nullable=is_null, is_primary=is_pk, default=default_value))

        return columns

    @staticmethod
    def _get_auto_column_name(con: sqlite3.Connection, name: str) -> str:
        """
        This function attempts to parse the SQL used to create the table in order to
        find the auto inc field, if one exists
        """
        cursor = con.cursor()
        row = cursor.execute(f"SELECT sql FROM sqlite_master where name = '{name}';").fetchone()
        if row:
            sql = row['sql']
            lines = [item.strip() for item in sql[sql.find("(")+1:sql.find(")")].split(',')]
            for line in lines:
                upper_line = line.upper()
                if 'AUTOINCREMENT' in upper_line:
                    return re.split("\s", line)[0].strip('"')

        return ''

    @staticmethod
    def _get_index_columns(con: sqlite3.Connection, name: str) -> list[str]:
        """
        This method extracts the column names for an index
        """
        cursor = con.cursor()
        names = list()

        rows = cursor.execute(f"PRAGMA index_info('{name}');").fetchall()
        if rows:
            for row in rows:
                names.append(row['name'])

        return names

    def _get_indexes(self, con: sqlite3.Connection, name: str) -> list[Index]:
        """
        This method extracts the indexes for a table
        """
        cursor = con.cursor()
        indexes = list()

        rows = cursor.execute(f"PRAGMA index_list('{name}');").fetchall()
        for row in rows:
            index_name = row['name']
            unique = bool(row['unique'])

            index = Index(index_name, is_unique=unique)
            columns = self._get_index_columns(con, index_name)
            index.columns.extend(columns)

            indexes.append(index)

        return indexes

    @staticmethod
    def _get_foreign_keys(con: sqlite3.Connection, name: str) -> list[ForeignKey]:
        """
        This method extracts the foreign keys for a table
        """
        cursor = con.cursor()
        keys = list()

        rows = cursor.execute(f"PRAGMA foreign_key_list('{name}');").fetchall()
        for row in rows:
            foreign_table = row['table']
            foreign_column = row['to']
            column = row['from']
            keys.append(ForeignKey('Unknown', column, foreign_table, foreign_column))

        return keys

    def _get_table(self, con: sqlite3.Connection, name: str) -> Table:
        """
        This method gets the table definition
        """
        tbl = Table(name)

        # Columns
        columns = self._get_table_columns(con, name)
        for column in columns:
            tbl.columns[column.name] = column

        # Check for auto inc column
        auto_col_name: str = self._get_auto_column_name(con, name)
        if auto_col_name and auto_col_name in tbl.columns:
            col = tbl.columns[auto_col_name]
            # noinspection PyDataclass
            tbl.columns[auto_col_name] = attrs.evolve(col, is_auto=True)

        # Indexes
        indexes = self._get_indexes(con, name)
        tbl.indexes.extend(indexes)

        # Foreign Keys
        fkeys = self._get_foreign_keys(con, name)
        tbl.foreign_keys.extend(fkeys)

        return tbl

    # endregion

    def extract(self, conn: IConnection) -> Database:
        con = sqlite3.connect(conn.host)
        con.row_factory = sqlite3.Row

        db = Database(conn.database, DatabaseType.SQLite)

        # Tables
        table_names = self._get_table_names(con)
        for name in table_names:
            db.tables[name] = self._get_table(con, name)

        # Views
        view_names = self._get_view_names(con)
        for name in view_names:
            db.views[name] = self._get_view(con, name)

        return db
