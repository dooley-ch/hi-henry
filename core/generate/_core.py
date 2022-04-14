# *******************************************************************************************
#  File:  _core.py
#
#  Created: 10-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  10-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['IDatabaseExplorer', 'IDatabase', 'ITable', 'IColumn']

from abc import abstractmethod
from typing import Protocol, Dict


class IColumn(Protocol):
    @property
    @abstractmethod
    def order(self) -> int:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def type(self) -> str:
        ...

    @property
    @abstractmethod
    def length(self) -> int:
        ...

    @property
    @abstractmethod
    def default(self) -> str | None:
        ...

    @property
    @abstractmethod
    def is_nullable(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_key(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_unique(self) -> bool:
        ...


class ITable(Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def columns(self) -> Dict[str, IColumn]:
        ...


class IDatabase(Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def tables(self) -> Dict[str, ITable]:
        ...


class IDatabaseExplorer(Protocol):
    def extract(self) -> IDatabase:
        ...
