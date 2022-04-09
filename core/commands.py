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

from argh import arg, named, confirm


@named('create')
@arg('database', help='The name of the database to use in the project')
@arg('user', help='The user account to use to connect to the database')
@arg('password', help='The user password to use to connect to the database')
def create_project(database: str, user: str, password: str, driver: str='mysql', host: str='127.0.0.1', port=3306):
    """
    This method creates a new project file using the supplied parameters
    :param database: The name of the database to use in the project
    :param user: The user account to use to connect to the database
    :param password: The user password to use to connect to the database
    :param driver: The database management system (DBMS) hostig the database
    :param host: The host where which the DBMS is running
    :param port: The port on which the DMBS is listening
    """
    return 'Create Project'


@named('delete')
@arg('database', help='The name of the database to use in the project')
def delete_project(database: str):
    """
    This method deletes an existing project
    :param database: The name of the database to use in the project
    """
    return 'Delete Project'

@named('generate')
@arg('database', help='The name of the database to use in the project')
def generate_code(database: str, folder: str | None = None):
    """
    This method generates the code for the given database
    :param database: The name of the database to use in the project
    :param folder: If provided, code will be generated in this folder
    """
    if confirm('Are you sure you wish to generate code', default=True):
        return 'Generate code'
    else:
        return "Don't generate code"


@named('clear')
def delete_code(folder: str | None = None):
    """
    This method deletes the generated code
    :param folder: If provided, code will be deleted from this folder
    """
    if confirm('Are you sure you wish to delete the code', default=True):
        return 'Delete code'
    else:
        return "Don't delete code"
