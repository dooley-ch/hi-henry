# *******************************************************************************************
#  File:  python_code_generator.py
#
#  Created: 23-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  23-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['initialize', 'MySqlCodeGenerator']

import pathlib
from datetime import datetime
from logging import Logger, getLogger
from typing import List

import mako.template as mako
import pydantic
import typer

import core.custom_types as types
from core.generate import register_generator_plugin


class _ColumnDefinition(pydantic.BaseModel):
    """
    This class holds the definition of a database table column
    """
    name: str
    definition: str

    class Config:
        arbitrary_types_allowed = True


class _ClassDefinition(pydantic.BaseModel):
    """
    This class holds the definition of a database table
    """
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


class MySqlCodeGenerator:
    """
    This class is responsible for generating python code based on the given database schema
    """
    @staticmethod
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
                                                       definition=MySqlCodeGenerator._get_data_type_definition(
                                                           col.name, col.type, col.length, data_map)))
            log.debug(f"Added column definition for table: {table.name} -> {col.name}")

        return class_def

    @staticmethod
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

    @staticmethod
    def _create_code_file_content(file_name: str, classes: List[types.IClassDefinition],
            templates_folder: pathlib.Path) -> List[str] | None:
        template_file: pathlib.Path = templates_folder.joinpath('default.tmpl')
        if not template_file.exists():
            return None

        engine = mako.Template(filename=str(template_file.absolute()))

        now = datetime.now()
        create_date: str = now.strftime("%d-%m-%Y")

        content: str = engine.render(file_name=file_name, create_date=create_date, classes=classes)

        content: List = content.splitlines(keepends=True)
        content.pop()
        content.pop()

        return content

    # noinspection PyUnusedLocal
    def generate(self, project_name: str, schema: types.IDatabase, datatype_map: types.DataTypeMap, output_folder: pathlib.Path,
            template_folder: pathlib.Path, multi_file: bool) -> bool:
        """
        This function generates the code for a project and writes it to the output folder
        """
        log: Logger = getLogger('progress_logger')
        error_log: Logger = getLogger()

        # Map schema to template classes
        classes: List[types.IClassDefinition] = list()
        try:
            with typer.progressbar(schema.tables) as work:
                for table in work:
                    class_def = self._build_class_definition(table, datatype_map)

                    log.info(f"Class definition generated for table: {table.name}")
                    classes.append(class_def)
        except Exception as e:
            error_log.exception(e)
            raise

        # Generate code
        try:
            output_file_name: str = f"_{project_name}_model.py"
            content: List[str] = MySqlCodeGenerator._create_code_file_content(output_file_name, classes, template_folder)
        except Exception as e:
            error_log.exception(e)
            return False

        # Write file
        output_file: pathlib.Path = output_folder.joinpath(output_file_name)
        with open(output_file, 'w') as file:
            try:
                file.writelines(content)
            except Exception as e:
                error_log.exception(e)
                return False

        return True


def initialize() -> None:
    """
    This function registers the plugin with the application
    """
    register_generator_plugin('python', MySqlCodeGenerator)
