# *******************************************************************************************
#  File:  _model.py
#
#  Created: 17-07-2022
#
#  History:
#  17-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['DatabaseType', 'DtoType', 'Project', 'ProjectList', 'ProjectDict']

from enum import Enum
from typing import NewType
import attrs


class DatabaseType(str, Enum):
    """
    Defines the database types
    """
    MySQL = "mysql"
    PostgreSQL = "postgresql"
    SQLite = "sqlite"


class DtoType(str, Enum):
    """
    Defines the DTO types
    """
    DataClasses = "dataclasses"
    Attrs = "attrs"
    Pydantic = "pydantic"


@attrs.frozen
class Project:
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    dbms: DatabaseType = attrs.field(validator=[attrs.validators.instance_of(DatabaseType)])
    dto: DtoType = attrs.field(validator=[attrs.field(validator=[attrs.validators.instance_of(DtoType)])])
    database: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    user: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    password: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    host: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    port: int = attrs.field(validator=[attrs.validators.instance_of(int)])


ProjectList = NewType("ProjectList", list[Project])

ProjectDict = NewType("ProjectDict", dict[str, Project])
