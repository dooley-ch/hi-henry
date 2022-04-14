# *******************************************************************************************
#  File:  __init__.py
#
#  Created: 10-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  10-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['build_file_content', 'IDatabaseExplorer', 'IDatabase', 'ITable', 'IColumn', 'register_plugin', 'unregister_plugin',
           'create_plugin', 'load_plugin']

from ._generate import build_file_content
from ._core import *
from ._schema_explorer_factory import *
