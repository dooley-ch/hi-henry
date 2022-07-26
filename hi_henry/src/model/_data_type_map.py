# *******************************************************************************************
#  File:  _data_type_map.py
#
#  Created: 24-07-2022
#
#  History:
#  24-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['DataTypeMap', 'StandardDataType']

from enum import Enum
import attrs
import pendulum


class StandardDataType(str, Enum):
    """
    This enum defines the standard data types
    """
    Binary = "Binary"
    Bit = "Bit"
    Boolean = "Boolean"
    Date = "Date"
    DateTime = "DateTime"
    Decimal = "Decimal"
    Double = "Double"
    Float = "Float"
    Integer = "Integer"
    String = "String"
    TimeStamp = "TimeStamp"


def _to_date(value: str) -> pendulum.DateTime | str:
    """
    Converts a string date value to a date/time value
    """
    if isinstance(value, str):
        return pendulum.parse(value, strict=False)
    return value


@attrs.frozen
class DataTypeMap:
    """
    This class holds the details of a data type mapping
    """
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    from_type: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    to_type: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    default_type: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    map: dict[str, str] = attrs.Factory(dict)
    lock_version: int = attrs.field(default=1, validator=[attrs.validators.instance_of(int), attrs.validators.ge(1)])
    created_at: pendulum.DateTime = attrs.field(factory=pendulum.now,
                                                validator=[attrs.validators.instance_of(pendulum.DateTime)],
                                                converter=_to_date)
    updated_at: pendulum.DateTime = attrs.field(factory=pendulum.now,
                                                validator=[attrs.validators.instance_of(pendulum.DateTime)],
                                                converter=_to_date)
