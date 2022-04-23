# *******************************************************************************************
#  File:  _explorer_factory.py
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
This module hands the management of database explorer plugins
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['register_plugin', 'unregister_plugin', 'create_explorer_plugin', 'load_plugin']

import importlib
from logging import Logger, getLogger
from typing import Dict

import custom_types
import core.custom_types as types


_plugin_creation_funcs: Dict[str, types.CreatePluginFunction] = dict()


def register_plugin(driver: str, create_function: types.CreatePluginFunction) -> None:
    """
    This function handles the registration of a plugin
    """
    _plugin_creation_funcs[driver] = create_function

    log: Logger = getLogger()
    log.debug(f"Plugin registered for driver: {driver}")


def unregister_plugin(driver: str) -> None:
    """
    This function handles the unregistration of a plugin
    """
    _plugin_creation_funcs.pop(driver, None)


def create_explorer_plugin(driver: str, conn_info: types.IDatabaseConnectionInfo) -> types.IDatabaseExplorer:
    """
    This function creates a new database explorer instance for a given driver
    """
    log: Logger = getLogger()

    if driver in _plugin_creation_funcs:
        func = _plugin_creation_funcs[driver]
        explorer = func(conn_info)

        log.debug(f"Explorer created for driver: {driver}")
        return explorer

    raise ValueError(f"No plugin available for driver: {driver}")


def load_plugin(module_name: str) -> None:
    """
    This function loads a moudule containing a plugin and initializes it
    """
    log: Logger = getLogger()

    try:
        plugin_module: custom_types.IPluginInterface = importlib.import_module(f"plugin.{module_name}")
        if plugin_module:
            log.debug(f"Plugin module loaded: {module_name}")
            plugin_module.initialize()
    except Exception as e:
        log.exception(e)
        raise
