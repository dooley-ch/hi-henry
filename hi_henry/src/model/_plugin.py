# *******************************************************************************************
#  File:  _plugin.py
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

__all__ = ['IConnection', 'IDatabaseExplorer', 'IPluginInterface', 'CreateExplorerPluginFunction']

import typing
from ._schema_interface import IDatabase


# noinspection PyPropertyDefinition
class IConnection(typing.Protocol):
    """
    This class defines the interface that must be implemented to support the connection to a database
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


class IDatabaseExplorer(typing.Protocol):
    """
    This interface provides access to the function needed to extract the database schema
    """

    def extract(self, conn: IConnection) -> IDatabase:
        ...


class IPluginInterface(typing.Protocol):
    """
    This is the interface all database explorer plugin modules must support
    """

    @staticmethod
    def initialize() -> None:
        ...


CreateExplorerPluginFunction: typing.TypeAlias = typing.Callable[..., IDatabaseExplorer]
