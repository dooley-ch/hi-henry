# *******************************************************************************************
#  File:  schema_explorer_factory_test.py
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

from pathlib import Path

import core.generate as generate
import core.system_config as config
import core.utils as utils


def test_load_and_create():
    file: Path = Path(__file__).parent.joinpath('config', 'mistral.env')
    conn_info: utils.ConnectionInfo = utils.get_config(file)

    plugins = config.get_plugins()
    for plugin in plugins:
        generate.load_plugin(plugin.file)

    explorer: generate.IDatabaseExplorer = generate.create_plugin('mysql', conn_info)
    assert explorer

    schema = explorer.extract()
    assert schema
