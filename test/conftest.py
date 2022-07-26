# *******************************************************************************************
#  File:  conftest.py
#
#  Created: 30-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  30-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

from pathlib import Path
import attrs
import pytest
from hi_henry.src.model import DataTypeMap
from hi_henry.src.data_maps import TypeMap


@pytest.fixture(scope="session")
def app_folder() -> Path:
    return Path(__file__).parent.joinpath('app_folder')


@pytest.fixture
def database_file_name(app_folder) -> Path:
    db_file = app_folder.joinpath('projects.json')
    if db_file.exists():
        db_file.unlink()

    return db_file


@pytest.fixture(scope="session")
def activity_log_file_name(app_folder) -> Path:
    return app_folder.joinpath('activity.log')


@pytest.fixture(scope="session")
def core_log_file_name(app_folder) -> Path:
    return app_folder.joinpath('core.log')


@pytest.fixture(scope="session")
def error_log_file_name(app_folder) -> Path:
    return app_folder.joinpath('error.log')


@pytest.fixture(scope="session")
def map_file_name(app_folder) -> Path:
    return app_folder.joinpath('map.cfg')


@attrs.frozen(kw_only=True)
class Connection:
    database: str | None = attrs.field(default=None)
    user: str | None = attrs.field(default=None)
    password: str | None = attrs.field(default=None)
    host: str = attrs.field(default="localhost")
    port: int | None = attrs.field(default=None)


@pytest.fixture(scope="session")
def sqlite_connection() -> Connection:
    database_file = Path(__file__).parent.joinpath('data', 'mistral.sqlite')
    return Connection(database="mistral", host=str(database_file.resolve()))


@pytest.fixture(scope="session")
def invalid_sqlite_connection() -> Connection:
    database_file = Path(__file__).parent.joinpath('data', 'mistral_xxx.sqlite')
    return Connection(database="mistral", host=str(database_file.resolve()))


@pytest.fixture(scope="session")
def mysql_connection() -> Connection:
    return Connection(database="mistral", user="root", password="mysql*347", port=3306)


@pytest.fixture(scope="session")
def invalid_mysql_connection() -> Connection:
    return Connection(database="new_mistral", user="root", password="mysql*347", port=3306)


@pytest.fixture(scope="session")
def postgresql_connection() -> Connection:
    return Connection(database="mistral", user='jdooley', port=5432)


@pytest.fixture(scope="session")
def invalid_postgresql_connection() -> Connection:
    return Connection(database="new_mistral", user='jdooley', port=5432)


@pytest.fixture
def data_maps_config_file() -> Path:
    return Path(__file__).parent.parent.joinpath('hi_henry', 'data', 'data_type_map.toml')


@pytest.fixture
def sample_data_map_1() -> DataTypeMap:
    record = DataTypeMap('SQLite_To_Standard', 'SQLite', 'Standard', 'String')
    record.map['INTEGER'] = 'Integer'
    record.map['REAL'] = 'Float'
    record.map['TEXT'] = 'String'
    record.map['BLOB'] = 'Binary'

    return record


@pytest.fixture
def sample_data_map_2() -> DataTypeMap:
    record = DataTypeMap("MySQL_To_Standard", "MySQL", 'Standard', 'String')
    record.map['INTEGER'] = 'Integer'
    record.map['REAL'] = 'Float'
    record.map['TEXT'] = 'String'
    record.map['BLOB'] = 'Binary'

    return record


@pytest.fixture(scope="session")
def sample_sqlite_type_map():
    map = TypeMap("SQLite_To_Standard", "SQLite", "Standard", "String")
    map['INTEGER'] = "Integer"
    map['REAL'] = "Float"
    map['TEXT'] = "String"
    map['BLOB'] = "Binary"

    return map


@pytest.fixture(scope="session")
def sample_mysql_type_map():
    map = TypeMap("MySQL_To_Standard", "MySQL", "Standard", "String")
    map['CHAR'] = 'String'
    map['VARCHAR'] = 'String'
    map['BINARY'] = 'String'
    map['VARBINARY'] = 'String'
    map['TINYBLOB'] = 'String'
    map['TINYTEXT'] = 'String'
    map['TEXT'] = 'String'
    map['BLOB'] = 'String'
    map['MEDIUMTEXT'] = 'String'
    map['MEDIUMBLOB'] = 'String'
    map['LONGTEXT'] = 'String'
    map['LONGBLOB'] = 'String'
    map['ENUM'] = 'String'
    map['BIT'] = 'Integer'
    map['TINYINT'] = 'Integer'
    map['BOOL'] = 'Integer'
    map['BOOLEAN'] = 'Integer'
    map['SMALLINT'] = 'Integer'
    map['MEDIUMINT'] = 'Integer'
    map['INT'] = 'Integer'
    map['INTEGER'] = 'Integer'
    map['BIGINT'] = 'Integer'
    map['FLOAT'] = "Float"
    map['DOUBLE'] = "Float"
    map['DECIMAL'] = "Decimal"
    map['DEC'] = "Float"
    map['DATE'] = "Date"
    map['DATETIME'] = "DateTime"
    map['TIMESTAMP'] = "TimeStamp"
    map['TIME'] = "DateTime"
    map['TIME'] = "Integer"

    return map
