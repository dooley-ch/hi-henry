# *******************************************************************************************
#  File:  __main__.py
#
#  Created: 09-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  09-04-2022: Initial version
#
# *******************************************************************************************

"""
This file contains the application entry point
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

from logging.config import fileConfig
import core.generate as generate
import core.system_config as config
import core.utils as utils
import core.command_line as command_line


def main():
    # Set up logging
    config_file = utils.get_config_folder().joinpath('logging.cfg')
    fileConfig(config_file)

    # Register plugins
    plugins = config.get_explorer_plugins()
    for plugin in plugins:
        generate.load_plugin(plugin.file)

    # Process commands
    command_line.app()


if __name__ == '__main__':
    main()
