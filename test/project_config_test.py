# *******************************************************************************************
#  File:  project_config_test.py
#
#  Created: 23-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  23-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import pathlib
import core.project_config as config

def test_list_projects():
    file = pathlib.Path(__file__).parent.joinpath('test_data', 'projects.toml')
    names = config.get_project_list(file)

    assert len(names) == 3


def test_get_project():
    file = pathlib.Path(__file__).parent.joinpath('test_data', 'projects.toml')
    project: config.ProjectDefinition = config.get_project('oak', file)

    assert project

