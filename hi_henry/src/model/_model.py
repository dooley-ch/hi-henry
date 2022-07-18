# *******************************************************************************************
#  File:  _model.py
#
#  Created: 17-07-2022
#
#  History:
#  17-07-2022: Initial version
#
# *******************************************************************************************
from __future__ import annotations

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['DatabaseType', 'DtoType', 'Project', 'ProjectList', 'ProjectDict', 'ProjectNameList', 'ProjectMetadata',
           'ProjectMetadataList']

from enum import Enum
from typing import NewType, Any
import attrs
import pendulum


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


def _to_date(value: str) -> pendulum.DateTime | str:
    if isinstance(value, str):
        return pendulum.parse(value, strict=False)
    return value


@attrs.frozen
class Project:
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    dbms: DatabaseType
    dto: DtoType
    database: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    user: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    password: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    host: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    port: int = attrs.field(validator=[attrs.validators.instance_of(int)])
    lock_version: int = attrs.field(default=1, validator=[attrs.validators.instance_of(int), attrs.validators.ge(1)])
    created_at: pendulum.DateTime = attrs.field(factory=pendulum.now,
                                                validator=[attrs.validators.instance_of(pendulum.DateTime)],
                                                converter=_to_date)
    updated_at: pendulum.DateTime = attrs.field(factory=pendulum.now,
                                                validator=[attrs.validators.instance_of(pendulum.DateTime)],
                                                converter=_to_date)

    def clone(self) -> Project:
        return Project(self.name, self.dbms, self.dto, self.database, self.user, self.password, self.host, self.port,
                       self.lock_version, self.created_at, self.updated_at)

ProjectList = NewType("ProjectList", list[Project])

ProjectDict = NewType("ProjectDict", dict[str, Project])

ProjectNameList = NewType("ProjectNameList", list[str])


@attrs.frozen
class ProjectMetadata:
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    lock_version: int = attrs.field(validator=[attrs.validators.instance_of(int)])
    created_at: pendulum.DateTime = attrs.field(validator=[attrs.validators.instance_of(pendulum.DateTime)],
                                                converter=_to_date)
    updated_at: pendulum.DateTime = attrs.field(validator=[attrs.validators.instance_of(pendulum.DateTime)],
                                                converter=_to_date)

    @classmethod
    def parse(cls, data: dict[str, Any]) -> ProjectMetadata:
        name = data['name']
        lock_version = data['lock_version']
        created_at = data['created_at']
        updated_at = data['updated_at']
        return ProjectMetadata(name, lock_version, created_at, updated_at)


ProjectMetadataList = NewType("ProjectMetadataList", list[ProjectMetadata])
