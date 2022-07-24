# *******************************************************************************************
#  File:  _postgresql_plugin.py
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

__all__ = ['PostgreSqlDatabaseExplorer']

from contextlib import contextmanager
from typing import Any

import attrs
import psycopg2
from ..model import ViewColumn, View, Column, Index, ForeignKey, Table, Database, IConnection, DatabaseType, \
    DatabaseInfo, SchemaInfo
from ..errors import DatabaseNotFoundError, SchemaNotFoundError


# noinspection SqlDialectInspection
class PostgreSqlDatabaseExplorer:
    """
    This class handles the extraction of the MySQL database schema
    """

    @staticmethod
    def _get_database_connection(con: IConnection) -> Any:
        """
        Returns a connection to a PostgreSQL database
        """
        return psycopg2.connect(
            f"dbname='{con.database}' user='{con.user}' password='{con.password}' host='{con.host}' port='{con.port}'")

    @contextmanager
    def _database_cursor(self, con: IConnection) -> Any:
        """
        This method returns am open database cursor
        """
        cursor = None

        try:
            db = self._get_database_connection(con)
            cursor = db.cursor()
            yield cursor
        finally:
            if cursor:
                cursor.close()

    def _get_database_details(self, con: IConnection) -> DatabaseInfo | None:
        """
        This method returns the database details
        """
        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT pd.oid AS id, pd.datname AS name, pa.rolname AS owner
                                FROM pg_database AS pd JOIN pg_authid pa on pd.datdba = pa.oid
                                WHERE (pd.datname = %s);""", (con.database,))
            row = cursor.fetchone()
            if row:
                rec_id = row[0]
                name = row[1]
                owner = row[2]
                return DatabaseInfo(rec_id, name, owner)

    def _get_schema_names(self, con: IConnection) -> dict[str, SchemaInfo]:
        """
        This method returns details of the database schema
        """
        schemas = dict()
        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT pn.oid AS id, pn.nspname AS name, pa.rolname AS owner 
                                FROM pg_namespace pn JOIN pg_authid pa on pn.nspowner = pa.oid;""")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    rec_id = row[0]
                    name = row[1]
                    owner = row[2]
                    schemas[name] = SchemaInfo(rec_id, name, owner)

        return schemas

    def _get_table_names(self, schema: str, con: IConnection) -> list[str]:
        """
        This method returns the table names
        """
        names = list()
        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT tablename AS name, tableowner AS owner
                                FROM pg_tables WHERE (schemaname = %s) ORDER BY tablename;""", (schema,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    name = row[0]
                    names.append(name)

            return names

    def _get_columns(self, name: str, schema: str, con: IConnection) -> list[Column]:
        """
        This method extracts the column details for a table
        """
        columns = list()
        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT ordinal_position AS "order", column_name AS name, data_type, 
                                character_maximum_length AS length, is_nullable, column_default AS default_value
                            FROM information_schema.columns
                                WHERE (table_catalog = %s) AND (table_schema = %s) AND (table_name = %s);""",
                           (con.database, schema, name))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    order = row[0]
                    col_name = row[1]
                    col_type = row[2]
                    length = row[3]
                    is_nullable = bool(row[4])
                    default = row[5]

                    is_auto = False
                    if default and 'nextval' in default:
                        is_auto = True

                    columns.append(Column(col_name, col_type, order, length,
                                          is_auto=is_auto, is_nullable=is_nullable, default=default))

        return columns

    def _get_table(self, name: str, schema: str, con: IConnection) -> Table:
        """
        This method extracts the table metadata
        """
        tbl = Table(name)

        columns = self._get_columns(name, schema, con)
        if columns:
            for column in columns:
                tbl.columns[column.name] = column

        indexes = self._get_indexes(name, con)
        if indexes:
            tbl.indexes.extend(indexes)

        # Fix up PK column flag
        for index in indexes:
            if index.is_primary:
                for column_name in index.columns:
                    col = tbl.columns[column_name]
                    # noinspection PyDataclass
                    tbl.columns[column_name] = attrs.evolve(col, is_primary=True, is_unique=True)
            break

        keys = self._get_foreign_keys(name, con)
        if keys:
            tbl.foreign_keys.extend(keys)

        return tbl

    def _get_index_columns(self, name: str, con: IConnection) -> list[str]:
        """
        This method gets the index column names
        """
        columns = list()

        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT attname AS name FROM pg_attribute pa JOIN pg_class pc on pc.oid = pa.attrelid
                                WHERE (pc.relname = %s);""", (name,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    columns.append(row[0])

        return columns

    def _get_indexes(self, name: str, con: IConnection) -> list[Index]:
        """
        This method gets the indexes for a table
        """
        indexes = list()

        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT pci.relname, pi.indisunique AS is_unique, pi.indisprimary AS is_pk 
                                FROM pg_index pi
                                JOIN pg_class pct on pct.oid = pi.indrelid
                                JOIN pg_class pci on pci.oid = pi.indexrelid
                                WHERE (pct.relname = %s);""", (name,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    name = row[0]
                    is_unique = row[1]
                    is_pk = row[2]
                    indexes.append(Index(name, is_unique=is_unique, is_primary=is_pk))

        for index in indexes:
            columns = self._get_index_columns(index.name, con)
            index.columns.extend(columns)

        return indexes

    def _get_foreign_keys(self, name: str, con: IConnection) -> list[ForeignKey]:
        """
        This method gets the foreign keys for a table
        """
        keys = list()

        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT tc.constraint_name AS name, kcu.column_name AS "column",
                                ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
                                FROM information_schema.table_constraints AS tc
                                    JOIN information_schema.key_column_usage AS kcu 
                                        ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = 
                                        kcu.table_schema
                                    JOIN information_schema.constraint_column_usage AS ccu
                                      ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
                                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name=%s;""", (name,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    fk_name = row[0]
                    column = row[1]
                    foreign_table = row[2]
                    foreign_column = row[3]

                    keys.append(ForeignKey(fk_name, column, foreign_table, foreign_column))

        return keys

    def _get_view_names(self, schema: str, con: IConnection) -> list[str]:
        """
        This method returns the table names
        """
        names = list()
        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT viewname AS name, viewowner AS owner FROM pg_views 
                                WHERE (schemaname = %s) ORDER BY viewname;""", (schema,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    name = row[0]
                    names.append(name)

            return names

    def _get_view(self, name: str, schema: str, con: IConnection) -> View | None:
        """
        This method extracts the table metadata from the database
        """
        view = View(name)

        columns = self._get_view_columns(name, schema, con)
        if columns:
            for column in columns:
                view.columns[column.name] = column

        return view

    def _get_view_columns(self, name: str, schema: str, con: IConnection) -> list[ViewColumn]:
        """
        This method extracts the column details for a table
        """
        columns = list()
        with self._database_cursor(con) as cursor:
            cursor.execute("""SELECT ordinal_position AS "order", column_name AS name, data_type,
                                character_maximum_length AS length
                                FROM information_schema.columns 
                                WHERE (table_catalog = %s) AND (table_schema = %s) 
                                AND (table_name = %s);""", (con.database, schema, name))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    order = row[0]
                    col_name = row[1]
                    col_type = row[2]
                    length = row[3]

                    columns.append(ViewColumn(col_name, col_type, order, length))

        return columns

    def extract(self, con: IConnection) -> Database | None:
        """
        This method extracts the database schema
        """

        # Make sure the database exists
        try:
            # check that the connection to the database works
            self._get_database_details(con)
        except psycopg2.OperationalError as ex:
            if 'does not exist' in str(ex):
                raise DatabaseNotFoundError(f"The following database could not be found: {con.database}")

        # Determine the schema to use and make sure it exists
        schema_name = 'public'
        schema_infos = self._get_schema_names(con)
        if con.database in schema_infos:
            schema_name = con.database
        if schema_name not in schema_infos:
            raise SchemaNotFoundError(f"The following schema could not be found: {schema_name}")

        db = Database(con.database, DatabaseType.PostgreSQL)

        # Tables
        table_names = self._get_table_names(schema_name, con)
        for table_name in table_names:
            table = self._get_table(table_name, schema_name, con)
            db.tables[table.name] = table

        # Views
        view_names = self._get_view_names(schema_name, con)
        for view_name in view_names:
            view = self._get_view(view_name, schema_name, con)
            db.views[view.name] = view

        return db
