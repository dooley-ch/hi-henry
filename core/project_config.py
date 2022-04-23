# *******************************************************************************************
#  File:  project_config.py
#
#  Created: 23-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  23-04-2022: Initial version
#
# *******************************************************************************************

"""
This module handles the management of project definitions
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['ProjectDefinition']

from pathlib import Path
from typing import List, Union, Dict
import pydantic
import tomli
import core.utils as utils

class ProjectDefinition(pydantic.BaseModel):
    name: str
    explorer: str
    generator: str
    host: str
    port: int
    database: str
    user: str
    password: str
    multi_file:bool


def _load_config(file: Union[Path, None] = None) -> Dict[str, List]:
    """
    This function loads the configuration information from the projects file
    """
    if file is None:
        file = utils.get_config_folder().joinpath('projects.toml')

    with open(file, "rb") as f:
        return tomli.load(f)


def get_project(name: str, file: Union[Path, None] = None) -> Union[ProjectDefinition]:
    data = _load_config(file)

    if 'projects' in data:
        projects: dict = data['projects']

        if (name in projects) and ('defaults' in data):
            project_data: dict = projects[name]
            defaults = data['defaults']
            project_data.update(defaults)

            return ProjectDefinition(**project_data)


def get_project_list(file: Union[Path, None] = None) -> Union[List, None]:
    """
    This function returns a list of projects defined in the application
    """
    data = _load_config(file)

    if 'projects' in data:
        projects: dict = data['projects']
        names: List[str] = list()

        for _, project in projects.items():
            name = project['name']
            names.append(name)

        names.sort()
        return names
