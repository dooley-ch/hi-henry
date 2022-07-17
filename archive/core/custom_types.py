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
__all__ = ['IDbConnInfo', 'IProject', 'IViewColumn', 'ViewColumns', 'IColumn', 'Columns', 'ColumnNames', 'IIndex',
           'IForeignKey', 'ITable', 'Tables', 'IView', 'Views', 'IDatabase', 'IDatabaseExplorer',
           'DataTypeMap', 'IGenerator', 'IPluginInterface',
           'CreateExplorerPluginFunction', 'CreateGeneratorPluginFunction',
           'IColumnDefinition', 'IClassDefinition']

import abc
import pathlib
from typing import Protocol, Union, TypeAlias, Dict, Callable, List, runtime_checkable


# noinspection PyPropertyDefinition
class IDbConnInfo(Protocol):
    """
    This class defines the interface that must be implemented to support the connection
    to a database
    """

    @property
    def database(self) -> str:
        ...

    @property
    def user(self) -> str:
        ...

    @property
    def password(self) -> str:
        ...

    @property
    def host(self) -> str:
        ...

    @property
    def port(self) -> int:
        ...


# noinspection PyPropertyDefinition
class IViewColumn(Protocol):
    """
    This interface defines a view columm
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
    def length(self) -> Union[int, None]:
        ...


ViewColumns: TypeAlias = List[IViewColumn]


# noinspection PyPropertyDefinition
class IColumn(IViewColumn):
    """
    This interface provides access to the column details needed to generate code
    """

    @property
    def default(self) -> Union[str, None]:
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


Columns: TypeAlias = List[IColumn]

ColumnNames: TypeAlias = List[str]


# noinspection PyPropertyDefinition
class IIndex(Protocol):
    """
    This class holds the index definition
    """

    @property
    def name(self) -> str:
        ...

    @property
    def columns(self) -> ColumnNames:
        ...

    @property
    def comment(self) -> Union[str, None]:
        ...


# noinspection PyPropertyDefinition
class IForeignKey:
    """
    This class holds the details of a foreign key
    """

    @property
    def name(self) -> str:
        ...

    @property
    def column_name(self) -> str:
        ...

    @property
    def foreign_column_name(self) -> str:
        ...

    @property
    def foreign_table_name(self) -> str:
        ...


# noinspection PyPropertyDefinition
class ITable(Protocol):
    """
    This interface provides access to the table details needed to generate code
    """

    @property
    def name(self) -> str:
        ...

    @property
    def comments(self) -> Union[str, None]:
        ...

    @property
    def rows(self) -> int:
        ...

    @property
    def primary_key(self) -> ColumnNames:
        ...

    @property
    def columns(self) -> dict[str, IColumn]:
        ...

    @property
    def unique_keys(self) -> dict[str, IIndex]:
        ...

    @property
    def indexes(self) -> dict[str, IIndex]:
        ...

    @property
    def foreign_keys(self) -> dict[str, IForeignKey]:
        ...


Tables: TypeAlias = List[ITable]


# noinspection PyPropertyDefinition
class IView(Protocol):
    """
    This interface provides access to the view details needed to generate code
    """

    @property
    def name(self) -> str:
        ...

    @property
    def comments(self) -> Union[str, None]:
        ...

    @property
    def columns(self) -> dict[str, IViewColumn]:
        ...


Views: TypeAlias = List[IView]


# noinspection PyPropertyDefinition
class IDatabase(Protocol):
    """
    This interface provides access to the database details needed to generate code
    """

    @property
    def name(self) -> str:
        ...

    @property
    def tables(self) -> Tables:
        ...

    def views(self) -> Views:
        ...


class IDatabaseExplorer(Protocol):
    """
    This interface provides access to the function needed to extract the database schema
    """

    def extract(self, conn_info: IDbConnInfo) -> IDatabase:
        ...


# noinspection PyPropertyDefinition
class IProject(IDbConnInfo):
    """
    This interface provides access to the project information
    """

    @property
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def explorer(self) -> str:
        ...

    @property
    def generator(self) -> str:
        ...

    @property
    def multi_file(self) -> bool:
        ...


DataTypeMap = Dict[str, str]


class IGenerator:
    """
    This class defines the interface for the code gemeratpr
    """

    def generate(self, project_name: str, schema: IDatabase, datatype_map: DataTypeMap, output_folder: pathlib.Path,
            template_folder: pathlib.Path, multi_file: bool) -> bool:
        ...


class IPluginInterface(Protocol):
    """
    This is the interface all database explorer plugin modules must support
    """

    @staticmethod
    def initialize() -> None:
        ...


CreateExplorerPluginFunction: TypeAlias = Callable[..., IDatabaseExplorer]
CreateGeneratorPluginFunction: TypeAlias = Callable[..., IGenerator]


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
