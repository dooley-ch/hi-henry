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

import archive.core.command_line as command_line
from archive import core as generate, core as config


def main():
    # Set up logging
    config.configure_logging()

    # Register plugins
    plugins = config.get_explorer_plugins()
    for plugin in plugins:
        generate.load_plugin(plugin.file)

    plugins = config.get_generator_plugins()
    for plugin in plugins:
        generate.load_plugin(plugin.file)

    # Process commands
    command_line.app()


if __name__ == '__main__':
    main()
