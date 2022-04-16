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

"""
This modlule impleents the code generation feature of the application
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['generate_code']

import pathlib
import pydantic
from typing import List
from logging import Logger, getLogger
import typer
import core.custom_types as types
import core.system_config as config
import core.utils as utils
from ._factory import create_plugin
from ._templates import create_code_file_content


class _ColumnDefinition(pydantic.BaseModel):
    name: str
    definition: str


class _ClassDefinition(pydantic.BaseModel):
    name: str
    columns: types.ColumnDefinitionList = list()

    class Config:
        arbitrary_types_allowed = True


def _build_class_name(value: str) -> str:
    """
    This function builds the class name from the table name
    """
    parts: List[str] = value.split('_')
    parts = [item.title() for item in parts]
    return "".join(parts)


def _get_data_type_definition(name: str, data_type: str, length: int, data_map: types.DataTypeMap) -> str:
    """
    This function builds the data type for the class attribute
    """
    if name in ['id', 'ID', 'lock_version', 'lock_version_id', 'record_id']:
        definition = "pydantic.PositiveInt"
    else:
        if data_type in data_map:
            definition = data_map[data_type]
        else:
            definition = data_map['default']

        if (definition == 'str') and (length > 0):
            definition = f"pydantic.constr(max_length={length})"

    return definition


def _build_class_definition(table: types.ITable, data_map: types.DataTypeMap) -> types.IClassDefinition:
    """
    This function builds the class definition to pass to the template engine, so it can create
    the class entry in the output file
    """
    log: Logger = getLogger()
    class_def = _ClassDefinition(name=_build_class_name(table.name))

    col: types.IColumn
    for col in table.columns:
        class_def.columns.append(_ColumnDefinition(name=col.name,
                                                   definition=_get_data_type_definition(col.name, col.type,
                                                                                        col.length, data_map)))
        log.debug(f"Added column definition for table: {table.name} -> {col.name}")

    return class_def


def generate_code(project: types.IProject, output_folder: pathlib.Path = None) -> str:
    """
    This function generates the code for a project and writes it to the output folder
    """
    log: Logger = getLogger('progress_logger')
    error_log: Logger = getLogger()

    explorer: types.IDatabaseExplorer = create_plugin(project.driver, project)
    schema: types.IDatabase = explorer.extract()

    data_map: types.DataTypeMap = config.get_data_map(project.driver)
    data_map.setdefault('default', 'str')

    # Map schema to template classes
    classes: List[types.IClassDefinition] = list()
    try:
        with typer.progressbar(schema.tables) as work:
            for table in work:
                class_def = _build_class_definition(table, data_map)

                log.info(f"Class definition generated for table: {table.name}")
                classes.append(class_def)
    except Exception as e:
        error_log.exception(e)
        raise

    # Generate code
    try:
        output_file_name: str = f"_{project.database}_model.py"
        content: List[str] = create_code_file_content(output_file_name, classes)
    except Exception as e:
        error_log.exception(e)
        raise

    # Write file
    if output_folder is None:
        output_folder = utils.get_output_folder()

    output_file: pathlib.Path = output_folder.joinpath(output_file_name)
    with open(output_file, 'w') as file:
        try:
            file.writelines(content)
        except Exception as e:
            error_log.exception(e)
            raise

    return "Code generated successfully"
