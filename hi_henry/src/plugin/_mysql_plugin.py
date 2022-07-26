# *******************************************************************************************
#  File:  _mysql_plugin.py
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

__all__ = ['MySQLDatabaseExplorer']

from contextlib import contextmanager
from mysql.connector import connect, MySQLConnection
from mysql.connector.cursor import MySQLCursorNamedTuple
from mysql.connector.errors import ProgrammingError
from ..data_maps import TypeMap
from ..model import ViewColumn, View, Column, Index, ForeignKey, Table, Database, IConnection, DatabaseType, \
    DatabaseMetadata, ViewMetaData, ViewColumnMetadata, TableMetaData, ColumnMetadata, IndexMetadata, \
    ForeignKeyMetadata, StandardDataType
from ..errors import DatabaseNotFoundError


# noinspection SqlDialectInspection
class MySQLDatabaseExplorer:
    """
    This class handles the extraction of the MySQL database schema
    """
    @staticmethod
    def _get_database_connection(con: IConnection) -> MySQLConnection:
        """
        Returns a connection to a MySQL database
        """
        return connect(user=con.user, password=con.password, host=con.host, port=con.port, database=con.database,
                       use_pure=True, consume_results=True)

    @contextmanager
    def _database_cursor(self, con: IConnection) -> MySQLCursorNamedTuple:
        """
        This method returns am open database cursor
        """
        cursor: MySQLCursorNamedTuple | None = None

        try:
            db = self._get_database_connection(con)
            cursor = db.cursor(named_tuple=True)
            yield cursor
        finally:
            if cursor:
                cursor.close()

    # region Views

    def _get_view_names(self, con: IConnection) -> list[str]:
        """
        This method returns the names of the views in a database
        """
        names = list()

        with self._database_cursor(con) as cursor:
            cursor.execute(f"""SELECT TABLE_NAME AS name FROM information_schema.tables
                                WHERE (TABLE_SCHEMA = %s) AND (TABLE_TYPE = 'VIEW')
                                ORDER BY TABLE_NAME;""", (con.database,))

            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    names.append(row.name)

        return names

    def _get_view_columns(self, view: str, con: IConnection) -> list[ViewColumn]:
        """
        This method extracts the column metadata for a view
        """
        columns = list()

        with self._database_cursor(con) as cursor:
            cursor.execute(f"""SELECT COLUMN_NAME AS name, ORDINAL_POSITION AS position, DATA_TYPE AS data_type,
                                    CHARACTER_MAXIMUM_LENGTH AS length  FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION;""",
                           (con.database, view))

            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    columns.append(ViewColumn(row.name, row.data_type.decode('UTF-8'), row.position, row.length))
            return columns

    def _get_view(self, name: str, con: IConnection) -> View:
        """
        This method extracts the table metadata from the database
        """
        view = View(name)

        cols = self._get_view_columns(name, con)
        for col in cols:
            view.columns[col.name] = col

        return view

    # endregion

    # region Tables

    def _get_table_names(self, database_name: str, con: IConnection) -> list[str]:
        """
        This method extracts the list of table names
        """
        names = list()

        with self._database_cursor(con) as cursor:
            cursor.execute(f"""SELECT TABLE_NAME AS name FROM information_schema.tables
                                WHERE (TABLE_SCHEMA = %s) AND (TABLE_TYPE = 'BASE TABLE') 
                                ORDER BY TABLE_NAME;""", (database_name,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    names.append(row.name)

        return names

    def _get_columns(self, table: str, con: IConnection) -> list[Column]:
        """
        This method extracts the column metadata for a given table
        """
        columns = list()

        with self._database_cursor(con) as cursor:
            cursor.execute(f"""SELECT COLUMN_NAME AS name, ORDINAL_POSITION AS position, COLUMN_DEFAULT AS default_value, 
                                    IS_NULLABLE AS is_null, DATA_TYPE AS data_type, CHARACTER_MAXIMUM_LENGTH AS length, 
                                    COLUMN_KEY AS col_key, EXTRA AS extra FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION;""",
                           (con.database, table))

            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    is_pk = row.col_key == 'PRI'
                    is_uk = row.col_key == 'UNI'
                    is_auto = row.extra == 'auto_increment'

                    default_value = None
                    if row.default_value:
                        default_value = row.default_value.decode('UTF-8')

                    columns.append(Column(row.name, row.data_type.decode('UTF-8'), row.position, row.length,
                                          bool(row.is_null), False, is_uk, is_auto, is_pk, default_value))
        return columns

    def _get_indexes(self, table: str, con: IConnection) -> list[Index]:
        """
        This method extracts the index metadata for a table
        """
        indexes = list()

        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT DISTINCT INDEX_NAME AS name, INDEX_COMMENT AS comment, !NON_UNIQUE AS is_unique
                                FROM INFORMATION_SCHEMA.STATISTICS
                                WHERE (TABLE_SCHEMA = %s) AND (TABLE_NAME = %s);""", (con.database, table))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    is_pk = False
                    if row.name == 'PRIMARY':
                        is_pk = True

                    ndx = Index(row.name, is_unique=bool(row.is_unique), is_primary=is_pk)
                    indexes.append(ndx)

            for index in indexes:
                cursor.execute("""SELECT COLUMN_NAME AS name FROM INFORMATION_SCHEMA.STATISTICS
                                WHERE (TABLE_SCHEMA = %s) AND (TABLE_NAME = %s) AND (INDEX_NAME = %s);""",
                               (con.database, table, index.name))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        index.columns.append(row.name)

        return indexes

    def _get_foreign_keys(self, table: str, con: IConnection) -> list[ForeignKey]:
        """
        This method extracts the foreign key metadata for a table
        """
        keys = list()

        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT CONSTRAINT_NAME AS name, COLUMN_NAME AS column_name,
                                REFERENCED_TABLE_NAME AS foreign_table, REFERENCED_COLUMN_NAME foreign_column
                                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                                WHERE (REFERENCED_TABLE_SCHEMA = %s) AND 
                                    (TABLE_NAME = %s) ORDER BY COLUMN_NAME;""", (con.database, table))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    keys.append(ForeignKey(row.name, row.column_name, row.foreign_table, row.foreign_column))

        return keys

    def _get_table(self, name: str, con: IConnection) -> Table:
        """
        This method extracts the table metadata from the database
        """
        tbl = Table(name)

        # Columns
        cols = self._get_columns(name, con)
        for col in cols:
            tbl.columns[col.name] = col

        # Indexes
        indexes = self._get_indexes(name, con)
        tbl.indexes.extend(indexes)

        # Foreign Keys
        keys = self._get_foreign_keys(name, con)
        tbl.foreign_keys.extend(keys)

        return tbl

    # endregion

    def _get_database_names(self, con: IConnection) -> list[str]:
        """
        This method returns a list of the databases on the server
        """
        names = list()

        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT SCHEMA_NAME AS name FROM INFORMATION_SCHEMA.SCHEMATA;""")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    names.append(row.name)

        return names

    def to_standard_schema(self, con: IConnection, type_map: TypeMap) -> DatabaseMetadata:
        """
        This method returns the database schema in a standard format
        """
        data = self.extract(con)

        meta = DatabaseMetadata(data.name, data.type)

        for _, view in data.views.items():
            m_view = ViewMetaData(view.name)
            for _, col in view.columns.items():
                data_type = StandardDataType(type_map[col.data_type.upper()])
                m_col = ViewColumnMetadata(col.name, data_type, col.order, col.length)
                m_view.columns[m_col.name] = m_col

            meta.views[m_view.name] = m_view

        for _, table in data.tables.items():
            m_table = TableMetaData(table.name)

            for _, col in table.columns.items():
                data_type = StandardDataType(type_map[col.data_type.upper()])
                m_col = ColumnMetadata(col.name, data_type, col.length, col.is_nullable, col.is_unique,
                                       col.is_auto, col.is_primary)
                m_table.columns[m_col.name] = m_col

            for index in table.indexes:
                m_index = IndexMetadata(index.name, is_primary=index.is_primary, is_unique=index.is_unique)
                m_index.columns.extend(index.columns)

                m_table.indexes.append(m_index)

            for key in table.foreign_keys:
                m_key = ForeignKeyMetadata(key.name, key.column, key.foreign_table, key.foreign_column)
                m_table.foreign_keys.append(m_key)

            meta.tables[m_table.name] = m_table

        return meta

    def extract(self, con: IConnection) -> Database:
        """
        This method extracts the database schema
        """
        try:
            # check that the connection to the database works
            self._get_database_names(con)
        except ProgrammingError as ex:
            if 'Unknown database' in str(ex):
                raise DatabaseNotFoundError(f"The following database could not be found: {con.database}")

        db = Database(con.database, DatabaseType.MySQL)

        # Views
        view_names = self._get_view_names(con)
        for name in view_names:
            db.views[name] = self._get_view(name, con)

        # Tables
        table_names = self._get_table_names(con.database, con)
        for name in table_names:
            db.tables[name] = self._get_table(name, con)

        return db
