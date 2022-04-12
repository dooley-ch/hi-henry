# *******************************************************************************************
#  File:  mysql_schema_test.py
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

from pathlib import Path

import pytest
import core.utils as utils
from plugin.mysql_schema_explorer import MySqlSchemaExplorer


@pytest.fixture()
def connection_info():
    file: Path = Path(__file__).parent.joinpath('config', 'eolas.env')
    return utils.get_config(file)


def test_idatabase(connection_info):
    explorer = MySqlSchemaExplorer()
    data = explorer.extract(connection_info)

    assert data
    assert len(data.tables) == 29

    table = data.tables['album']
    assert table
    assert len(table.columns) == 7
