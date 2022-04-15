# *******************************************************************************************
#  File:  mysql_schema_explorer.py
#
#  Created: 12-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  12-04-2022: Initial version
#
# *******************************************************************************************

"""
This plugin is used to extract the schema from a mysql database
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['MySqlSchemaExplorer']

from abc import abstractmethod
from typing import Protocol, Dict
from contextlib import contextmanager
from mysql.connector import connect, MySQLConnection, DatabaseError
from mysql.connector.cursor import MySQLCursor, MySQLCursorDict
from logging import Logger, getLogger
import pydantic
from core.generate import register_plugin


class _ConnectionInfo(Protocol):
    """
    This class defines the interface that must be implemented to support the connection
    to a database
    """
    @property
    @abstractmethod
    def database(self) -> str:
        ...

    @property
    @abstractmethod
    def user(self) -> str:
        ...

    @property
    @abstractmethod
    def driver(self) -> str:
        ...

    @property
    @abstractmethod
    def password(self) -> str:
        ...

    @property
    @abstractmethod
    def host(self) -> str:
        ...

    @property
    @abstractmethod
    def port(self) -> int:
        ...


class _Column(pydantic.BaseModel):
    """
    This class is used to return the definition of a column in a  MySQL database
    """
    order: pydantic.PositiveInt
    name: str
    type: str
    length: int = 0
    default: str | None
    is_nullable: bool = True
    is_key: bool = False
    is_unique: bool = False


class _Table(pydantic.BaseModel):
    """
    This class is used to return the definition of a table in a MySQL database
    """
    name: str
    columns: Dict[str, _Column] = dict()


class _Database(pydantic.BaseModel):
    """
    This class is used to return the definition of a schema in a MySQL database
    """
    name: str
    tables: Dict[str, _Table] = dict()


class MySqlSchemaExplorer:
    """
    This class is used to extract the schema of a database in a MySQL database
    """
    _log: Logger
    _conn_info: _ConnectionInfo

    def __init__(self, conn_info: _ConnectionInfo):
        """
        Creates an instance of the class with the given parameters
        """
        self._log = getLogger('MySqlSchemaExplorer')
        self._conn_info = conn_info

    @staticmethod
    def get_database_connection(conn_info: _ConnectionInfo) -> MySQLConnection:
        """
        Returns a connection to a MySQL database
        """
        return connect(user=conn_info.user, password=conn_info.password, host=conn_info.host,
                       port=conn_info.port, database=conn_info.database, use_pure=True,
                       consume_results=True)

    @contextmanager
    def open_database(self, context: str) -> MySQLConnection:
        """
        This method provides an open database context manager
        """
        conn: MySQLConnection | None = None

        try:
            conn = self.get_database_connection(self._conn_info)

            yield conn
        except DatabaseError as ex:
            self._log.error(f"Failed to open database conection ({context}) - {ex}")
            raise
        finally:
            if conn:
                if conn.is_connected():
                    conn.close()

    @contextmanager
    def open_database_cursor(self, context: str, named_tuple: bool = False,
            dictionary: bool = False):
        """
        This method returns am open cursor context manager
        """
        cursor: MySQLCursor

        with self.open_database(context) as db:
            try:
                if named_tuple:
                    cursor = db.cursor(named_tuple=True)
                elif dictionary:
                    cursor = db.cursor(dictionary=True)
                else:
                    cursor = db.cursor()

                yield cursor
            except DatabaseError as ex:
                self._log.error(f"Failed to open cursor ({context}) - {ex}")
                raise
            finally:
                if cursor:
                    cursor.close()

    @staticmethod
    def _extract_tables(cursor: MySQLCursorDict, db: _Database):
        """
        This method extacts the table definitions from the database
        """
        cursor.execute(''"SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = %s;""", (db.name,))
        table_names = cursor.fetchall()
        if table_names:
            for table_name in table_names:
                name = table_name['TABLE_NAME']
                table = _Table(name=name)
                db.tables[table.name] = table

    @staticmethod
    def extract_columns(cursor: MySQLCursorDict, db_name: str, table: _Table):
        """
        This method extrcts the column definitions for a table from the database
        """
        cursor.execute("""SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, COLUMN_DEFAULT, IS_NULLABLE, 
                                    COLUMN_KEY, EXTRA FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION;""", (db_name, table.name))

        rows = cursor.fetchall()
        for index, entry in enumerate(rows):
            name = entry['COLUMN_NAME']
            data_type = entry['DATA_TYPE'].decode('UTF-8')
            length = 0 if entry['CHARACTER_MAXIMUM_LENGTH'] is None else int(entry['CHARACTER_MAXIMUM_LENGTH'])
            default = entry['COLUMN_DEFAULT']
            is_nullable = bool(entry['IS_NULLABLE'])
            column_key = entry['COLUMN_KEY']
            order = index + 1

            is_key = False
            if column_key:
                if column_key == 'PRI':
                    is_key = True

            is_unique = False
            if column_key:
                if column_key == 'UNI':
                    is_unique = True

            column = _Column(order=order, name=name, type=data_type, length=length, default=default,
                             is_nullable=is_nullable, is_key=is_key, is_unique=is_unique)
            table.columns[column.name] = column

    def extract(self) -> _Database | None:

        db = _Database(name=self._conn_info.database)

        cursor: MySQLCursorDict
        with self.open_database_cursor('extract', dictionary=True) as cursor:
            self._extract_tables(cursor, db)
            for item in db.tables.items():
                MySqlSchemaExplorer.extract_columns(cursor, db.name, item[1])

        return db


def initialize() -> None:
    """
    This function registers the plugin with the application
    """
    register_plugin('mysql', MySqlSchemaExplorer)
