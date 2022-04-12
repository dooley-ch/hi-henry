# *******************************************************************************************
#  File:  _generate_mysql.py
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
__all__ = ['MySqlSchemaExtractor']

import core.utils as utils
from ._core import IDatabase


class MySqlSchemaExtractor:
    _conn_info: utils.ConnectionInfo

    def __init__(self, conn_info: utils.ConnectionInfo):
        self._conn_info = conn_info

    def extract(self) -> IDatabase | None:
        pass
