# *******************************************************************************************
#  File:  errors.py
#
#  Created: 18-07-2022
#
#  History:
#  18-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['DuplicateRecordError', 'RecordNotFoundError', 'DatabaseNotFoundError', 'SchemaNotFoundError']


class AppError(Exception):
    """
    Base class for all application exceptions
    """
    pass


class DuplicateRecordError(AppError):
    """
    Raised when the record already exists in the database
    """
    pass


class RecordNotFoundError(AppError):
    """
    Raised when there is no record to update
    """
    pass


class DatabaseNotFoundError(AppError):
    """
    Raised when the DBMS does not contain the required database
    """
    pass


class SchemaNotFoundError(DatabaseNotFoundError):
    """
    Raised when the DBMS does not contain the required schema
    """
    pass
