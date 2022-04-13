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

import argh
import core.commands as commands
import core.generate as generate
import core.system_config as config


def main():
    # Register plugins
    plugins = config.get_plugins()
    for plugin in plugins:
        generate.load_plugin(plugin.file)

    # Set up the command line parser
    cmd_parser: argh.ArghParser = argh.ArghParser()
    cmd_parser.add_commands([commands.create_project, commands.delete_project, commands.generate_code,
                             commands.delete_code])

    # Execute requested command
    cmd_parser.dispatch()


if __name__ == '__main__':
    main()
