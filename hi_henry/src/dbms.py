# *******************************************************************************************
#  File:  dbms.py
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

__all__ = []

import typing
import pathlib
import pendulum
import tinydb
import attrs
from .model import Project, ProjectMetadata, ProjectMetadataList
from .errors import DuplicateRecordError, RecordNotFoundError


class Database:
    """
    This class provides access to the application's database
    """
    _db: tinydb.TinyDB

    def __init__(self, file: pathlib.Path):
        """
        Initializes an instance of the class by creating a connection to the database
        """
        self._db = tinydb.TinyDB(file)

    @staticmethod
    def _record_to_dict(record: Project) -> dict[str, typing.Any]:
        """
        This method converts the project record into a dictionary to store in the database
        """
        data = attrs.asdict(record)
        data['dbms'] = record.dbms.value
        data['dto'] = record.dto.value
        data['created_at'] = record.created_at.to_iso8601_string()
        data['updated_at'] = record.updated_at.to_iso8601_string()
        return data

    def get_projects(self) -> ProjectMetadataList | None:
        """
        This method returns the metadata for the projects stored in the database
        """
        data = self._db.all()
        if data:
            records = ProjectMetadataList(list())
            for item in data:
                records.append(ProjectMetadata.parse(item))
            return records

    def get(self, name: str) -> Project | None:
        """
        Returns the requested project if it exists
        """
        data = self._db.search(tinydb.where("name") == name)
        if data:
            data = data[0]
            return Project(**data)

    def insert(self, record: Project) -> int:
        """
        Inserts a new project record in the database
        """
        if self.get(record.name):
            raise DuplicateRecordError(f"A project with the name: {record.name} already exists in the database")

        data = self._record_to_dict(record)
        return self._db.insert(data)

    def update(self, record: Project) -> None:
        """
        Updates an existing record in the database
        """
        if not self.get(record.name):
            raise RecordNotFoundError(f"A project with the name: {record.name} does not exist")

        data = self._record_to_dict(record)
        data['lock_version'] = data['lock_version'] + 1
        data['updated_at'] = pendulum.now().to_iso8601_string()

        self._db.update(data, tinydb.where("name") == record.name)
