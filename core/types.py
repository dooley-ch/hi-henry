# *******************************************************************************************
#  File:  types.py
#
#  Created: 24-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  24-04-2022: Initial version
#
# *******************************************************************************************

"""
This module defines the customs data types used by the application
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = []

from abc import abstractmethod
from typing import List, Dict, Union, Protocol


class IViewColumn(Protocol):
    """
    This interface defines the data needed to define a column in a view
    """
    @abstractmethod
    @property
    def name(self) -> str:
        ...

    @abstractmethod
    @property
    def data_type(self) -> str:
        ...

    @abstractmethod
    @property
    def order(self) -> int:
        ...


class IColumn(IViewColumn):
    """
    This interface defines the data needed to define a column in a table
    """
    @abstractmethod
    @property
    def length(self) -> int:
        ...

    @abstractmethod
    @property
    def default(self) -> Union[str, None]:
        ...

    @abstractmethod
    @property
    def is_nullable(self) -> bool:
        ...


class IPrimaryKey(Protocol):
    columns: List[str]


class IIndex(IPrimaryKey):
    columns: List[str]


class IUniqueKey(IIndex):
    pass


class IForeignKey(Protocol):
    column: str
    foreign_table: str
    foreign_column: str


class ITable(Protocol):
    @abstractmethod
    @property
    def columns(self) -> Dict[str, IColumn]:
        ...

    @abstractmethod
    @property
    def primary_key(self) -> IPrimaryKey:
        ...

    @abstractmethod
    @property
    def unique_keys(self) -> List[IUniqueKey]:
        ...

    @abstractmethod
    @property
    def foreign_keys(self) -> List[IForeignKey]:
        ...

    @abstractmethod
    @property
    def indexes(self) -> List[IIndex]:
        ...


class IView(Protocol):
    @abstractmethod
    @property
    def columns(self) -> Dict[str, IViewColumn]:
        ...


class IDatabase(Protocol):
    @abstractmethod
    @property
    def name(self) -> str:
        ...

    @abstractmethod
    @property
    def tables(self) -> Dict[str, ITable]:
        ...

    @abstractmethod
    @property
    def views(self) -> Dict[str, ITable]:
        ...
