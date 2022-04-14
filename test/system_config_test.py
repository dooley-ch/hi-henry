# *******************************************************************************************
#  File:  system_config_test.py
#
#  Created: 13-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  13-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import core.system_config as config


def test_get_plugins() -> None:
    plugins = config.get_plugins()

    assert plugins
    assert len(plugins) >= 1


def test_get_data_map() -> None:
    map = config.get_data_map('mysql')

    assert map
