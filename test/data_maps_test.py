# *******************************************************************************************
#  File:  data_maps_test.py
#
#  Created: 24-07-2022
#
#  History:
#  24-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = []

import hi_henry.src.data_maps as dm

def test_load_config(data_maps_config_file) -> None:
    data = dm.load_config(data_maps_config_file)
    assert len(data) == 4
