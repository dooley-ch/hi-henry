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
__all__ = ['write_code']

import pathlib
from logging import Logger, getLogger
import core.utils as utils
from ._schema_explorer_factory import create_plugin
from ._core import IDatabaseExplorer, IDatabase, ITable, IColumn


def _write_code(schema: IDatabase, output_folder: pathlib.Path) -> bool:
    error_log: Logger = getLogger()
    progress_log: Logger = getLogger('progress_logger')

    progress_log.info(f"Started generating code for: {schema.name}")
    progress_log.info(f"Output folder: {output_folder}")

    table: ITable
    for _, table in schema.tables.items():
        progress_log.info(f"Created code for table: {table.name}")

        column: IColumn
        for _, column in table.columns.items():
            progress_log.debug(f"Created code for column: {column.name}")

    progress_log.info(f"Ended generating code for: {schema.name}")
    return False


def write_code(connection_info: utils.ConnectionInfo, output_folder: pathlib.Path) -> str:
    db_explorer: IDatabaseExplorer = create_plugin(connection_info.driver, connection_info)
    schema: IDatabase = db_explorer.extract()

    if _write_code(schema, output_folder):
        log: Logger = getLogger()
        log.info(f"Generated code for database: {connection_info.database}")
        return "\nCode generated"

    return "\nFailed to generate code, see log for details"
