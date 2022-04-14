# *******************************************************************************************
#  File:  _generate.py
#
#  Created: 11-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  11-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['build_file_content']

import pathlib
from logging import Logger, getLogger
from typing import List, Dict
import core.utils as utils
import core.template_engine as engine
import core.system_config as config
from ._schema_explorer_factory import create_plugin
from ._core import IDatabaseExplorer, IDatabase, ITable, IColumn


def _create_class_def(table: ITable, data_type_map: Dict[str, str]) -> engine.ClassDefinition:
    data_type_map.setdefault('default', 'str')

    # Create class name
    parts: List[str] = table.name.split('_')
    parts = [item.title() for item in parts]
    class_name: str = "".join(parts)

    # Create definition
    class_def = engine.ClassDefinition(name=class_name)

    for _, item in table.columns.items():
        if item.name in ['id', 'ID', 'lock_version', 'lock_version_id', 'record_id']:
            definition = "pydantic.PositiveInt"
        else:
            if item.type in data_type_map:
                definition: str = data_type_map[item.type]
            else:
                definition: str = data_type_map['default']

            if (definition == 'str') and (item.length > 0):
                definition = f"pydantic.constr(max_length={item.length})"

        column = engine.ColumnDefinition(name=item.name, definition=definition)
        class_def.columns.append(column)

    return class_def


def _write_code(schema: IDatabase, output_folder: pathlib.Path) -> bool:
    output_file_name: str = f"_{schema.name}_model.py"
    error_log: Logger = getLogger()
    progress_log: Logger = getLogger('progress_logger')
    map: Dict[str, str] = config.get_data_map('mysql')

    progress_log.info(f"Started generating code for: {schema.name}")
    progress_log.info(f"Output folder: {output_folder}")

    classes = list()

    table: ITable
    for _, table in schema.tables.items():
        progress_log.info(f"Created code for table: {table.name}")
        classes.append(_create_class_def(table, map))

    file_content: List[str] = engine.create_code_file_content(file_name=output_file_name, classes=classes)

    output_file: pathlib.Path = utils.get_output_folder().joinpath(output_file_name)
    with open(output_file, 'w') as file:
        file.writelines(file_content)

    progress_log.info(f"Ended generating code for: {schema.name}")
    return False


def build_file_content(connection_info: utils.ConnectionInfo, output_folder: pathlib.Path) -> str:
    db_explorer: IDatabaseExplorer = create_plugin(connection_info.driver, connection_info)
    schema: IDatabase = db_explorer.extract()

    if _write_code(schema, output_folder):
        log: Logger = getLogger()
        log.info(f"Generated code for database: {connection_info.database}")
        return "\nCode generated"

    return "\nFailed to generate code, see log for details"
