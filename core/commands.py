# *******************************************************************************************
#  File:  commands.py
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
This module provides the command line methods and parameters supported by the application
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['create_project', 'delete_project', 'generate_code', 'delete_code']

from logging import Logger, getLogger
from datetime import datetime
from pathlib import Path
from argh import arg, named, confirm
import core.utils as utils
import core.generate as generate


@named('create')
@arg('database', help='The name of the database to use in the project')
@arg('user', help='The user account to use to connect to the database')
@arg('password', help='The user password to use to connect to the database')
def create_project(database: str, user: str, password: str, driver: str = 'mysql',
        host: str = '127.0.0.1', port=3306) -> None:
    """
    This method creates a new project file using the supplied parameters
    :param database: The name of the database to use in generating code
    :param user: The name of the database to use in generating code
    :param password: The user password to use to connect to the database
    :param driver: The database management system (DBMS) hostig the database
    :param host: The host where which the DBMS is running
    :param port: The port on which the DMBS is listening
    """
    file: Path = utils.get_config_folder().joinpath(f"{database.lower()}.env")
    if file.exists():
        return f"A configuration for the database: {database.lower()}, exists."

    now: datetime = datetime.now()
    now_str: str = now.strftime("%m/%d/%Y, %H:%M:%S")

    contents: list[str] = [
        f"# Hi-Henry Configuration File: {now_str}\n",
        f"HIH_DATABASE={database}\n",
        f"HIH_USER={user}\n",
        f"HIH_PASSWORD={password}\n",
        f"HIH_DRIVER={driver}\n",
        f"HIH_HOST={host}\n"
        f"HIH_PORT={port}"
    ]

    with open(file, 'w') as f:
        f.writelines(contents)

    log: Logger = getLogger()
    log.info(f"Configuration file created for: {database}")

    return 'Configuration file created'


@named('delete')
@arg('database', help='The name of the database to use in the project')
def delete_project(database: str) -> None:
    """
    This method deletes an existing project
    :param database: The name of the database to use in the project
    """
    file: Path = utils.get_config_folder().joinpath(f"{database.lower()}.env")
    if not file.exists():
        return f"No configuration file exists for the database: {database.lower()}."

    file.unlink()

    log: Logger = getLogger()
    log.info(f"Configuration file deleted: {database}")

    return 'File deleted successfully'


@named('generate')
@arg('database', help='The name of the database to use in the project')
def generate_code(database: str, folder: str | None = None) -> None:
    """
    This method generates the code for the given database
    :param database: The name of the database to use in the project
    :param folder: If provided, code will be generated in this folder
    """
    file: Path = utils.get_config_folder().joinpath(f"{database.lower()}.env")
    if not file.exists():
        return f"No configuration file exists for the database: {database.lower()}."

    if confirm('Are you sure you wish to generate code', default=True):
        # Ensure the output folder exists
        output_folder: Path = utils.get_output_folder()
        if folder:
            output_folder = folder
        if not output_folder.exists():
            output_folder.mkdir(parents=True, exist_ok=True)

        # Get the connection info
        connection_info = utils.get_config(file)

        # Generate code
        return generate.build_file_content(connection_info, output_folder)

    return "No code generated"


@named('clear')
def delete_code(folder: str | None = None) -> None:
    """
    This method deletes the generated code
    :param folder: If provided, code will be deleted from this folder
    """
    # Make sure the folder and contents exists
    output_folder: Path = utils.get_output_folder()
    if folder:
        output_folder = folder
    if not output_folder.exists():
        return f"Code folder not found: {output_folder}."

    # Makre sure there are files to delete
    files = list(output_folder.glob('*.py'))

    if files:
        if confirm('Are you sure you wish to delete the code', default=True):
            for file in files:
                file.unlink()

    log: Logger = getLogger()
    log.info(f"Code deleted from folder: {output_folder}")

    return "No code files deleted."
