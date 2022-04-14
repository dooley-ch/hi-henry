# *******************************************************************************************
#  File:  template_engine.py
#
#  Created: 14-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  14-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['create_code_file_content', 'ClassDefinition', 'ColumnDefinition']

import pathlib
from datetime import datetime
from typing import List
import core.utils as utils
import mako.template as mako
import pydantic


class ColumnDefinition(pydantic.BaseModel):
    name: str
    definition: str


class ClassDefinition(pydantic.BaseModel):
    name: str
    columns: List[ColumnDefinition] = list()


def create_code_file_content(file_name: str, classes: List[ClassDefinition]) -> List[str] | None:
    template_file: pathlib.Path = utils.get_templates_folder().joinpath('default.tmpl')
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
