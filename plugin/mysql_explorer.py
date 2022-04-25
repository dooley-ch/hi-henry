# *******************************************************************************************
#  File:  mysql_explorer.py
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
__all__ = ['MySQLExplorer']

from contextlib import contextmanager
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import Optional
from mysql.connector import connect, MySQLConnection
from mysql.connector.cursor import MySQLCursorNamedTuple
import core.custom_types as types
from core.generate import register_explorer_plugin


@dataclass(frozen=True)
class ViewColumn:
    """
    This class holds details of a column in a view defined by the database schema
    """
    name: str
    data_type: str
    order: int = field(default=0)
    length: Optional[int] = None


@dataclass(frozen=True)
class Column:
    """
    This class holds details of a column in a table defined by the database schema
    """
    name: str
    data_type: str
    order: int = field(default=0)
    length: int = field(default=0)
    default: str = field(default='')
    is_nullable: bool = field(default=False)
    is_unique: bool = field(default=False)
    is_auto: bool = field(default=False)
    is_primary: bool = field(default=False)


@dataclass()
class Index:
    """
    This class holds the index definition
    """
    name: str
    comment: Optional[str] = None
    columns: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ForeignKey:
    """
    This class holds the details of a foreign key
    """
    name: str
    column_name: str
    foreign_column_name: str
    foreign_table_name: str


@dataclass()
class Table:
    """
    This class holds the definition of a database table
    """
    name: str
    comment: str = ''
    row: int = 0
    primary_key: list[str] = field(default_factory=list)
    columns: dict[str, Column] = field(default_factory=dict)
    unique_keys: dict[str, Index] = field(default_factory=dict)
    indexes: dict[str, Index] = field(default_factory=dict)
    foreign_keys: dict[str, ForeignKey] = field(default_factory=dict)


@dataclass(frozen=True)
class View:
    """
    This class holds the definition of a database view
    """
    name: str
    comment: str = ''
    columns: dict[str, ViewColumn] = field(default_factory=dict)


@dataclass(frozen=True)
class DatabaseSchema:
    """
    This class acts as a container for the database scheama
    """
    name: str
    tables: dict[str, Table] = field(default_factory=dict)
    views: dict[str, View] = field(default_factory=dict)


class MySQLExplorer:
    """
    This class implements a plugin to provied the schema for a MySQL database
    """
    @staticmethod
    def _get_database_connection(conn_info: types.IDbConnInfo) -> MySQLConnection:
        """
        Returns a connection to a MySQL database
        """
        return connect(user=conn_info.user, password=conn_info.password, host=conn_info.host,
                       port=conn_info.port, database=conn_info.database, use_pure=True,
                       consume_results=True)

    @contextmanager
    def _open_database_cursor(self, conn_info: types.IDbConnInfo):
        """
        This method returns am open database cursor
        """
        cursor: MySQLCursorNamedTuple = None

        try:
            db = MySQLExplorer._get_database_connection(conn_info)
            cursor = db.cursor(named_tuple=True)
            yield cursor
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def _database_not_found(database_name: str, cursor: MySQLCursorNamedTuple) -> bool:
        cursor.execute("SELECT SCHEMA_NAME AS name FROM information_schema.schemata;")
        rows = cursor.fetchall()
        if rows:
            names = [row.name for row in rows]
            if database_name in names:
                return False

    @staticmethod
    def _get_table_names(database_name: str, cursor: MySQLCursorNamedTuple) -> list[str] | None:
        cursor.execute(f"""SELECT TABLE_NAME AS name FROM information_schema.tables
                                WHERE (TABLE_SCHEMA = %s) AND (TABLE_TYPE = 'BASE TABLE') 
                                ORDER BY TABLE_NAME;""", (database_name,))
        rows = cursor.fetchall()
        if rows:
            return [row.name for row in rows]

    @staticmethod
    def _get_view_names(database_name: str, cursor: MySQLCursorNamedTuple) -> list[str] | None:
        cursor.execute(f"""SELECT TABLE_NAME AS name FROM information_schema.tables
                                WHERE (TABLE_SCHEMA = %s) AND (TABLE_TYPE = 'VIEW') 
                                ORDER BY TABLE_NAME;""", (database_name,))
        rows = cursor.fetchall()
        if rows:
            return [row.name for row in rows]

    @staticmethod
    def _get_table_columns(table_name: str, cursor: MySQLCursorNamedTuple, database_name: str) -> dict[str, Column]:
        """
        This method adds the column definitions to the table
        """
        columns: dict[str, Index] = dict()

        cursor.execute(f"""SELECT COLUMN_NAME AS name, ORDINAL_POSITION AS position, COLUMN_DEFAULT AS default_value, 
                                IS_NULLABLE AS is_null, DATA_TYPE AS data_type, CHARACTER_MAXIMUM_LENGTH AS length, 
                                COLUMN_KEY AS col_key, EXTRA AS extra
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION;""",
                       (database_name, table_name))

        rows = cursor.fetchall()
        if rows:
            for row in rows:
                is_pk = row.col_key == 'PRI'
                is_uk = row.col_key == 'UNI'
                is_auto = row.extra == 'auto_increment'

                col = Column(row.name, row.data_type.decode('UTF-8'), row.position, row.length, row.default_value,
                             bool(row.is_null), is_uk, is_auto, is_pk)
                columns[col.name] = col

        return columns

    @staticmethod
    def _get_view_columns(view_name: str, cursor: MySQLCursorNamedTuple, database_name: str) -> dict[str, Column]:
        """
        This method adds the column definitions to the view
        """
        columns: dict[str, Index] = dict()

        cursor.execute(f"""SELECT COLUMN_NAME AS name, ORDINAL_POSITION AS position, DATA_TYPE AS data_type,
                                CHARACTER_MAXIMUM_LENGTH AS length  FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION;""",
                       (database_name, view_name))

        rows = cursor.fetchall()
        if rows:
            for row in rows:
                col = ViewColumn(row.name, row.data_type, row.position, row.length)
                columns[col.name] = col

        return columns

    @staticmethod
    def _get_primary_key(columns: dict[str, Column]) -> list[str]:
        cols: list[str] = list()

        for _, col in columns.items():
            if col.is_primary:
                cols.append(col.name)

        return cols

    @staticmethod
    def _get_indexes(table_name: str, cursor: MySQLCursorNamedTuple,
            database_name: str, non_unique: int) -> dict[str, Index]:
        """
        This method extrcts the indexes for the table
        """
        indexes: dict[str, Index] = dict()

        cursor.execute("""SELECT DISTINCT INDEX_NAME AS name, INDEX_COMMENT AS comment
                            FROM INFORMATION_SCHEMA.STATISTICS
                            WHERE (TABLE_SCHEMA = %s) AND (TABLE_NAME = %s) AND
                                  (INDEX_NAME != 'PRIMARY') AND (NON_UNIQUE = %s);""",
                       (database_name, table_name, non_unique))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                index = Index(row.name, row.comment)
                indexes[index.name] = index
        else:
            return

        for name in indexes:
            cursor.execute("""SELECT COLUMN_NAME AS name FROM INFORMATION_SCHEMA.STATISTICS
                                WHERE (TABLE_SCHEMA = %s) AND (TABLE_NAME = %s) AND
                                    (INDEX_NAME != 'PRIMARY') AND (INDEX_NAME = %s);""",
                           (database_name, table_name, name))

            rows = cursor.fetchall()
            if rows:
                names = [row.name for row in rows]
                indexes[name].columns = names

        return indexes

    @staticmethod
    def _get_unique_keys(table_name: str, cursor: MySQLCursorNamedTuple, database_name: str) -> dict[str, Index]:
        """
        This method extrcts the unique keys for the table
        """
        return MySQLExplorer._get_indexes(table_name, cursor, database_name, 0)

    @staticmethod
    def _get_other_indexes(table_name: str, cursor: MySQLCursorNamedTuple, database_name: str) -> dict[str, Index]:
        """
        This method extrcts the non-uniqu4 indexes for the table
        """
        return MySQLExplorer._get_indexes(table_name, cursor, database_name, 1)

    @staticmethod
    def _get_foreign_keys(table_name: str, cursor: MySQLCursorNamedTuple, database_name: str) -> dict[str, ForeignKey]:
        """
        This method extracts the foreign keys
        """
        foreign_keys: dict[str, ForeignKey] = dict()

        cursor.execute("""SELECT CONSTRAINT_NAME AS name, COLUMN_NAME AS column_name,
                                REFERENCED_TABLE_NAME AS foreign_table, REFERENCED_COLUMN_NAME foreign_column
                            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                            WHERE (REFERENCED_TABLE_SCHEMA = %s) AND 
                                (TABLE_NAME = %s) ORDER BY COLUMN_NAME;""",
                       (database_name, table_name))

        rows = cursor.fetchall()
        if rows:
            for row in rows:
                fk = ForeignKey(row.name, row.column_name, row.foreign_column, row.foreign_table)
                foreign_keys[fk.name] = fk

        return foreign_keys

    @staticmethod
    def _get_table_schema(table_name: str, cursor: MySQLCursorNamedTuple, database_name: str) -> Table | None:
        cursor.execute("""SELECT TABLE_COMMENT AS comment, TABLE_ROWS AS row_count FROM information_schema.tables
                            WHERE (TABLE_SCHEMA = %s) AND (TABLE_TYPE = 'BASE TABLE') 
                                AND (TABLE_NAME = %s);""", (database_name, table_name))
        row = cursor.fetchone()
        if row:
            # Create the table
            table = Table(table_name, row.comment, row.row_count)

            # Add columns
            data = MySQLExplorer._get_table_columns(table_name, cursor, database_name)
            if data:
                table.columns.update(data)

            # Add Primary key
            data = MySQLExplorer._get_primary_key(table.columns)
            if data:
                table.primary_key = data

            # Add Unique keys
            data = MySQLExplorer._get_unique_keys(table_name, cursor, database_name)
            if data:
                table.unique_keys.update(data)

            # Add Indexes
            data = MySQLExplorer._get_other_indexes(table_name, cursor, database_name)
            if data:
                table.indexes.update(data)

            # Add Foreign keys
            data = MySQLExplorer._get_foreign_keys(table_name, cursor, database_name)
            if data:
                table.foreign_keys.update(data)

            return table

    @staticmethod
    def _get_view_schema(view_name: str, cursor: MySQLCursorNamedTuple, database_name: str) -> View | None:
        cursor.execute("""SELECT TABLE_COMMENT AS comment FROM information_schema.tables
                            WHERE (TABLE_SCHEMA = %s) AND (TABLE_TYPE = 'VIEW') 
                                AND (TABLE_NAME = %s);""", (database_name, view_name))
        row = cursor.fetchone()
        if row:
            # Create the view
            view = View(view_name, row.comment)

            # Add columns
            data = MySQLExplorer._get_view_columns(view_name, cursor, database_name)
            if data:
                view.columns.update(data)

            return view

    def extract(self, conn_info: types.IDbConnInfo) -> DatabaseSchema:
        """
        This method manages the extraction of the database schema
        """
        log_progress: Logger = getLogger('progress_logger')

        table_count: int = 0
        view_count: int = 0

        log_progress.info(f"*** Extracting schema for: {conn_info.database}***")

        database = DatabaseSchema(conn_info.database)

        cursor: MySQLCursorNamedTuple
        with self._open_database_cursor(conn_info) as cursor:
            if MySQLExplorer._database_not_found(conn_info.database, cursor):
                raise ValueError(f"MySQLExplorer: Database not found: {conn_info.database}")

            table_names = MySQLExplorer._get_table_names(conn_info.database, cursor)
            if table_names:
                for name in table_names:
                    table = MySQLExplorer._get_table_schema(name, cursor, conn_info.database)
                    database.tables[name] = table
                    table_count += 1
                    log_progress.info(f"Schema extracted for table: {name}")

            view_names = MySQLExplorer._get_view_names(conn_info.database, cursor)
            if view_names:
                for name in view_names:
                    view = MySQLExplorer._get_view_schema(name, cursor, conn_info.database)
                    database.views[name] = view
                    view_count += 1
                    log_progress.info(f"Schema extracted for view: {name}")

        log_progress.info(f"*** Schema Extraction completed: tables - {table_count}, views - {view_count} ***")

        return database


def initialize() -> None:
    """
    This function registers the plugin with the application
    """
    log: Logger = getLogger()

    register_explorer_plugin('mysql', MySQLExplorer)
    log.debug('Explorer plugin registered: MySQLExplorer')
