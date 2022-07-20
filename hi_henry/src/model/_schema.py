# *******************************************************************************************
#  File:  _schema.py
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

__all__ = ['ViewColumn', 'ViewColumns', 'View', 'ViewList', 'Column', 'Columns', 'ColumnNames',
           'Index', 'Indexes', 'ForeignKey', 'ForeignKeys', 'Table', 'TableList', 'Database']

import typing
import attrs
from ._model import DatabaseType


@attrs.frozen
class ViewColumn:
    """
    This class holds the view column definition
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    data_type: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    order: int = attrs.field(validator=[attrs.validators.instance_of(int)])
    length: int | None = attrs.field(default=None,validator=[attrs.validators.optional(attrs.validators.instance_of(int))])
    comment: str | None = attrs.field(default=None,
                                      validator=attrs.validators.optional(attrs.validators.instance_of(str)))


ViewColumns: typing.TypeAlias = dict[str, ViewColumn]


@attrs.frozen
class View:
    """
    This class holds the view definition
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    columns: ViewColumns = attrs.Factory(dict)
    comment: str | None = attrs.field(default=None,
                                      validator=attrs.validators.optional(attrs.validators.instance_of(str)))


ViewList: typing.TypeAlias = dict[str, View]


@attrs.frozen
class Column:
    """
    This class holds the definition of a table column
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    data_type: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    order: int = attrs.field(validator=[attrs.validators.instance_of(int)])
    length: int | None = attrs.field(default=None,validator=[attrs.validators.optional(attrs.validators.instance_of(int))])
    is_nullable: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_key: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_unique: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_auto: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_primary: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    default: str | None = attrs.field(default=None,
                                      validator=attrs.validators.optional(attrs.validators.instance_of(str)))
    comment: str | None = attrs.field(default=None,
                                      validator=attrs.validators.optional(attrs.validators.instance_of(str)))


Columns: typing.TypeAlias = dict[str, Column]

ColumnNames: typing.TypeAlias = list[str]


@attrs.frozen
class Index:
    """
    This class holds the index definition
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    columns: ColumnNames = attrs.Factory(list)
    is_unique: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    is_primary: bool = attrs.field(default=False, validator=[attrs.validators.instance_of(bool)])
    comment: str | None = attrs.field(default=None,
                                      validator=attrs.validators.optional(attrs.validators.instance_of(str)))


Indexes: typing.TypeAlias = list[Index]


@attrs.frozen
class ForeignKey:
    """
    This class holds the definition of a foreign key
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    column: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    foreign_table: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    foreign_column: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    comment: str | None = attrs.field(default=None,
                                      validator=attrs.validators.optional(attrs.validators.instance_of(str)))


ForeignKeys = typing.TypeAlias = list[ForeignKey]


@attrs.frozen
class Table:
    """
    This class holds the definition of a table
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    columns: Columns = attrs.Factory(dict)
    indexes: Indexes = attrs.Factory(list)
    foreign_keys: ForeignKeys = attrs.Factory(list)
    comment: str | None = attrs.field(default=None,
                                      validator=attrs.validators.optional(attrs.validators.instance_of(str)))


TableList: typing.TypeAlias = dict[str, Table]


@attrs.frozen
class Database:
    """
    This class holds the database definition
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    type: DatabaseType
    tables: TableList = attrs.Factory(dict)
    views: ViewList = attrs.Factory(dict)
