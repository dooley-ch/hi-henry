# *******************************************************************************************
#  File:  _schema_explorer_factory.py
#
#  Created: 13-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  13-04-2022: Initial version
#
# *******************************************************************************************

"""
This module hands the management of schema explorer plugins
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['register_plugin', 'unregister_plugin', 'create_plugin', 'load_plugin']

import importlib
from typing import Dict, Callable, Protocol
from core.utils import ConnectionInfo
from ._core import IDatabaseExplorer

_plugin_creation_funcs: Dict[str, Callable[..., IDatabaseExplorer]] = dict()


class PluginInterface(Protocol):
    """
    This is the interface all database explorer plugin modules must support
    """
    @staticmethod
    def initialize() -> None:
        ...

def register_plugin(driver: str, create_function: Callable[..., IDatabaseExplorer]) -> None:
    """
    This function handles the registration of a plugin
    """
    _plugin_creation_funcs[driver] = create_function


def unregister_plugin(driver: str) -> None:
    """
    This function handles the unregistration of a plugin
    """
    _plugin_creation_funcs.pop(driver, None)


def create_plugin(driver: str, conn_info: ConnectionInfo) -> IDatabaseExplorer:
    """
    This function creates a new database explorer instance for a given driver
    """
    if driver in _plugin_creation_funcs:
        func = _plugin_creation_funcs[driver]
        return func(conn_info)

    raise ValueError(f"No plugin available for driver: {driver}")

def load_plugin(module_name: str) -> None:
    plugin_module: PluginInterface = importlib.import_module(f"plugin.{module_name}")
    if plugin_module:
        plugin_module.initialize()
