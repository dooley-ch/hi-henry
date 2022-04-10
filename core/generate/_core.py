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
__all__ = ['generate_code', 'IDatabase', 'ITable', 'IView', 'IProcedure', 'IParam', 'IColumn', 'IIndex', 'IForeignKey']

from typing import Protocol, List
import pathlib
import core.utils as utils


class IParam(Protocol):
    def order(self) -> int:
        ...

    def name(self) -> str:
        ...

    def type(self) -> str:
        ...


class IColumn(Protocol):
    def order(self) -> int:
        ...

    def name(self) -> str:
        ...

    def type(self) -> str:
        ...

    def param(self) -> str:
        ...


class IIndex(Protocol):
    def name(self) -> str:
        ...

    def type(self) -> str:
        ...

    def unique(self) -> bool:
        ...

    def columns(self) -> List[IColumn]:
        ...


class IForeignKey(Protocol):
    def name(self) -> str:
        ...

    def columns(self) -> List[IColumn]:
        ...

    def foreign_table(self) -> str:
        ...

    def foreign_columns(self) -> List[IColumn]:
        ...


class IProcedure(Protocol):
    def name(self) -> str:
        ...

    def params(self) -> List[IParam]:
        ...

    def columns(self) -> List[IColumn]:
        ...


class IView(Protocol):
    def name(self) -> str:
        ...

    def columns(self) -> List[IColumn]:
        ...


class ITable(Protocol):
    def name(self) -> str:
        ...

    def columns(self) -> List[IColumn]:
        ...

    def indexes(self) -> List[IIndex]:
        ...

    def foreign_keys(self) -> List[IForeignKey]:
        ...


class IDatabase(Protocol):
    def name(self) -> str:
        ...

    def procedures(self) -> List[IProcedure]:
        ...

    def views(self) -> List[IView]:
        ...

    def tables(self) -> List[ITable]:
        ...


def generate_code(connection_info: utils.ConnectionInfo, output_folder: pathlib.Path) -> str:
    return 'Generation not implemented'
