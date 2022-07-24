# *******************************************************************************************
#  File:  _schema_interface.py
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

__all__ = ['IViewColumn', 'IViewColumns', 'IView', 'IViewList', 'IColumn', 'IColumns', 'IColumnNames',
           'IIndex', 'IIndexes', 'IForeignKey', 'IForeignKeys', 'ITable', 'ITableList', 'IDatabase']

import typing
from ._model import DatabaseType


# noinspection PyPropertyDefinition
@typing.runtime_checkable
class IViewColumn(typing.Protocol):
    """
    This interface defines a view column
    """

    @property
    def name(self):
        ...

    @property
    def data_type(self) -> str:
        ...

    @property
    def order(self) -> int:
        ...

    @property
    def length(self) -> int | None:
        ...

    @property
    def comment(self) -> str | None:
        ...


IViewColumns: typing.TypeAlias = dict[str, IViewColumn]


# noinspection PyPropertyDefinition
@typing.runtime_checkable
class IView(typing.Protocol):
    """
    This interface defines a view
    """
    @property
    def name(self) -> str:
        ...

    @property
    def columns(self) -> IViewColumns:
        ...

    @property
    def comment(self) -> str | None:
        ...


IViewList: typing.TypeAlias = dict[str, IView]


# noinspection PyPropertyDefinition
@typing.runtime_checkable
class IColumn(typing.Protocol):
    """
    This interface provides access to the column details needed to generate code
    """
    @property
    def name(self):
        ...

    @property
    def data_type(self) -> str:
        ...

    @property
    def order(self) -> int:
        ...

    @property
    def length(self) -> int | None:
        ...

    @property
    def default(self) -> str | None:
        ...

    @property
    def is_nullable(self) -> bool:
        ...

    @property
    def is_key(self) -> bool:
        ...

    @property
    def is_unique(self) -> bool:
        ...

    @property
    def is_auto(self) -> bool:
        ...

    @property
    def is_primary(self) -> bool:
        ...

    @property
    def comment(self) -> str | None:
        ...


IColumns: typing.TypeAlias = list[IColumn]

IColumnNames: typing.TypeAlias = list[str]


# noinspection PyPropertyDefinition
@typing.runtime_checkable
class IIndex(typing.Protocol):
    """
    This class holds the index definition
    """
    @property
    def name(self) -> str:
        ...

    @property
    def columns(self) -> IColumnNames:
        ...

    @property
    def is_unique(self) -> bool:
        ...

    @property
    def is_primary(self) -> bool:
        ...

    @property
    def comment(self) -> str | None:
        ...


IIndexes: typing.TypeAlias = list[IIndex]


# noinspection PyPropertyDefinition
@typing.runtime_checkable
class IForeignKey(typing.Protocol):
    """
    This class holds the details of a foreign key
    """
    @property
    def name(self) -> str:
        ...

    @property
    def column(self) -> str:
        ...

    @property
    def foreign_column(self) -> str:
        ...

    @property
    def foreign_table(self) -> str:
        ...

    @property
    def comment(self) -> str | None:
        ...


IForeignKeys = typing.TypeAlias = list[IForeignKey]


# noinspection PyPropertyDefinition
@typing.runtime_checkable
class ITable(typing.Protocol):
    """
    This class holds the definition of a table
    """
    @property
    def name(self) -> str:
        ...

    @property
    def columns(self) -> IColumns:
        ...

    @property
    def indexes(self) -> IIndexes:
        ...

    @property
    def foreign_keys(self) -> IForeignKeys:
        ...

    @property
    def comment(self) -> str | None:
        ...


ITableList: typing.TypeAlias = dict[str, ITable]


# noinspection PyPropertyDefinition
@typing.runtime_checkable
class IDatabase(typing.Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def type(self) -> DatabaseType:
        ...

    @property
    def tables(self) -> ITableList:
        ...

    @property
    def views(self) -> IViewList:
        ...

    @property
    def comment(self) -> str | None:
        ...
