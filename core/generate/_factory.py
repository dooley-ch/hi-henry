# *******************************************************************************************
#  File:  _factory.py
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
__all__ = ['register_explorer_plugin', 'unregister_explorer_plugin', 'create_explorer_plugin',
           'register_generator_plugin', 'unregister_generator_plugin', 'create_generator_plugin', 'load_plugin']

import importlib
from logging import Logger, getLogger
from typing import Dict

import custom_types
import core.custom_types as types

_plugin_explorer_creation_funcs: Dict[str, types.CreateExplorerPluginFunction] = dict()
_plugin_generator_creation_funcs: Dict[str, types.CreateGeneratorPluginFunction] = dict()
_log: Logger = getLogger()


def register_generator_plugin(name: str, create_function: types.CreateGeneratorPluginFunction) -> None:
    """
    This function handles the registration of a generator plugin
    """
    _plugin_generator_creation_funcs[name] = create_function
    _log.debug(f"Plugin registered for generator: {name}")


def unregister_generator_plugin(name: str) -> None:
    """
    This function handles the unregistration of a plugin
    """
    _plugin_generator_creation_funcs.pop(name, None)
    _log.debug(f"Plugin unregistered for generator: {name}")


def create_generator_plugin(name: str) -> types.IGenerator:
    """
    This function creates a new generator instance for a given name
    """
    if name in _plugin_explorer_creation_funcs:
        func = _plugin_generator_creation_funcs[name]
        explorer = func()

        _log.debug(f"Generator created for: {name}")
        return explorer

    raise ValueError(f"No generator plugin available for: {name}")


def register_explorer_plugin(name: str, create_function: types.CreateExplorerPluginFunction) -> None:
    """
    This function handles the registration of an explorer plugin
    """
    _plugin_explorer_creation_funcs[name] = create_function
    _log.debug(f"Plugin registered for explorer: {name}")


def unregister_explorer_plugin(name: str) -> None:
    """
    This function handles the unregistration of a plugin
    """
    _plugin_explorer_creation_funcs.pop(name, None)
    _log.debug(f"Plugin unregistered for explorer: {name}")


def create_explorer_plugin(name: str, conn_info: types.IDatabaseConnectionInfo) -> types.IDatabaseExplorer:
    """
    This function creates a new database explorer instance for a given name
    """
    if name in _plugin_explorer_creation_funcs:
        func = _plugin_explorer_creation_funcs[name]
        explorer = func(conn_info)

        _log.debug(f"Explorer created for: {name}")
        return explorer

    raise ValueError(f"No explorer plugin available for: {name}")


def load_plugin(module_name: str) -> None:
    """
    This function loads a moudule containing a plugin and initializes it
    """
    try:
        plugin_module: custom_types.IPluginInterface = importlib.import_module(f"plugin.{module_name}")
        if plugin_module:
            _log.debug(f"Plugin module loaded: {module_name}")
            plugin_module.initialize()
    except Exception as e:
        _log.exception(e)
        raise
