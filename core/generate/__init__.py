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
__all__ = ['write_code', 'IDatabaseExplorer', 'IDatabase', 'ITable', 'IColumn']

from ._generate import write_code
from ._core import *