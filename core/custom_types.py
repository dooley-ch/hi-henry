# *******************************************************************************************
#  File:  custom_types.py
#
#  Created: 15-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  15-04-2022: Initial version
#
# *******************************************************************************************

"""
Tbis module contains the definition of custom types used in the application
"""
__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['IColumn', 'ColumnList', 'ITable', 'TableList', 'IDatabase', 'IDatabaseExplorer', 'IPluginInterface',
           'IDatabaseConnectionInfo', 'CreatePluginFunction', 'IProject', 'IColumnDefinition', 'IClassDefinition',
           'DataTypeMap']

import abc
from typing import Protocol, Union, TypeAlias, Dict, Callable, List, runtime_checkable


class IColumn(Protocol):
    """
    This interface provides access to the column details needed to generate code
    """
    @property
    @abc.abstractmethod
    def order(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def type(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def length(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def default(self) -> Union[str, None]:
        ...

    @property
    @abc.abstractmethod
    def is_nullable(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def is_key(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def is_unique(self) -> bool:
        ...


ColumnList: TypeAlias = List[IColumn]


class ITable(Protocol):
    """
    This interface provides access to the table details needed to generate code
    """
    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def columns(self) -> ColumnList:
        ...


TableList: TypeAlias = List[ITable]


class IDatabase(Protocol):
    """
    This interface provides access to the database details needed to generate code
    """
    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def tables(self) -> TableList:
        ...


class IDatabaseExplorer(Protocol):
    """
    This interface provides access to the function needed to extract the database schema
    """
    def extract(self) -> IDatabase:
        ...


class IPluginInterface(Protocol):
    """
    This is the interface all database explorer plugin modules must support
    """

    @staticmethod
    def initialize() -> None:
        ...


class IDatabaseConnectionInfo(Protocol):
    """
    This class defines the interface that must be implemented to support the connection
    to a database
    """

    @property
    @abc.abstractmethod
    def database(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def user(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def driver(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def password(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def host(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def port(self) -> int:
        ...


class IProject(IDatabaseConnectionInfo):
    """
    This interface provides access to the project information
    """
    @property
    @abc.abstractmethod
    def driver(self) -> str:
        ...


CreatePluginFunction: TypeAlias = Callable[[IDatabaseConnectionInfo], IDatabaseExplorer]


@runtime_checkable
class IColumnDefinition(Protocol):
    """
    This class defines the column interface
    """
    name: str
    definition: str


ColumnDefinitionList: TypeAlias = List[IColumnDefinition]


@runtime_checkable
class IClassDefinition(Protocol):
    """
    This class defines the class interface
    """
    name: str
    columns: ColumnDefinitionList = list()


DataTypeMap = Dict[str, str]
