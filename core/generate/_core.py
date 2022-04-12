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

from typing import Protocol, Dict
import core.utils as utils


class IColumn(Protocol):
    def order(self) -> int:
        ...

    def name(self) -> str:
        ...

    def type(self) -> str:
        ...

    def length(self) -> int:
        ...

    def default(self) -> str | None:
        ...

    def is_nullable(self) -> bool:
        ...

    def is_key(self) -> bool:
        ...

    def is_unique(self) -> bool:
        ...


class ITable(Protocol):
    def name(self) -> str:
        ...

    def columns(self) -> Dict[str, IColumn]:
        ...


class IDatabase(Protocol):
    def name(self) -> str:
        ...

    def tables(self) -> Dict[str, ITable]:
        ...


class IDatabaseExplorer(Protocol):
    def extract(self, conn_info: utils.ConnectionInfo) -> IDatabase:
        ...
