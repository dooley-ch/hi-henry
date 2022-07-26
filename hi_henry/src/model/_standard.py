# *******************************************************************************************
#  File:  _standard.py
#
#  Created: 25-07-2022
#
#  History:
#  25-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['DatabaseMetadata', 'TableMetaData', 'ColumnMetadata', 'IndexMetadata', 'ForeignKeyMetadata',
           'ViewMetaData', 'ViewColumnMetadata']

import attrs
from ._model import DatabaseType
from ._data_type_map import StandardDataType


@attrs.frozen
class ColumnMetadata:
    """
    This class holds the metadata for a table column
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    data_type: StandardDataType = attrs.field(validator=[attrs.validators.instance_of(StandardDataType)])
    length: int | None = attrs.field(default=None,
                                     validator=[attrs.validators.optional(attrs.validators.instance_of(int))])
    is_nullable: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_unique: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_auto: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_primary: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])


@attrs.frozen
class IndexMetadata:
    """
    This class holds the index definition
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    columns: list[str] = attrs.Factory(list)
    is_unique: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_primary: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])


@attrs.frozen
class ForeignKeyMetadata:
    """
    This class holds the definition of a foreign key
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    column: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    foreign_table: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    foreign_column: str = attrs.field(validator=[attrs.validators.instance_of(str)])


@attrs.frozen
class TableMetaData:
    """
    This class holds the metadata for a table
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    columns: dict[str, ColumnMetadata] = attrs.Factory(dict)
    indexes: list[IndexMetadata] = attrs.Factory(list)
    foreign_keys: list[ForeignKeyMetadata] = attrs.Factory(list)


@attrs.frozen
class ViewColumnMetadata:
    """
    This class holds the metadata fora view column
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    data_type: StandardDataType = attrs.field(validator=[attrs.validators.instance_of(StandardDataType)])
    order: int = attrs.field(validator=[attrs.validators.instance_of(int)])
    length: int | None = attrs.field(default=None,
                                     validator=[attrs.validators.optional(attrs.validators.instance_of(int))])


@attrs.frozen
class ViewMetaData:
    """
    This class holds the metadata for a view
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    columns: dict[str, ViewColumnMetadata] = attrs.Factory(dict)


@attrs.frozen
class DatabaseMetadata:
    """
    This class holds the metadata for a database
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    type: DatabaseType
    tables: dict[str, TableMetaData] = attrs.Factory(dict)
    views: dict[str, ViewMetaData] = attrs.Factory(dict)
