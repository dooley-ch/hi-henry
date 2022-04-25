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
import core.custom_types as types
import core.system_config as config
import core.utils as utils
from ._factory import create_explorer_plugin, create_generator_plugin


def generate_code(project: types.IProject, output_folder: pathlib.Path = None) -> bool:
    """
    This function generates the code for a project and writes it to the output folder
    """
    explorer: types.IDatabaseExplorer = create_explorer_plugin(project.explorer)
    schema: types.IDatabase = explorer.extract(project)

    data_map: types.DataTypeMap = config.get_data_map(project.explorer)
    data_map.setdefault('default', 'str')

    generator: types.IGenerator = create_generator_plugin(project.generator)

    return generator.generate(project.name, schema, data_map, output_folder, utils.get_templates_folder(),
                              project.multi_file)
