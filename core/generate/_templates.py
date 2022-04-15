# *******************************************************************************************
#  File:  _templates.py
#
#  Created: 15-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  15-04-2022: Initial version
#
# *******************************************************************************************

"""
This module hands populate of the code template from the data supplied
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['create_code_file_content']

import pathlib
from datetime import datetime
from typing import List
import mako.template as mako
import core.utils as utils
import core.custom_types as types


def create_code_file_content(file_name: str, classes: List[types.IClassDefinition]) -> List[str] | None:
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
