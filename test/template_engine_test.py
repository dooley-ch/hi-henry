# *******************************************************************************************
#  File:  template_engine_test.py
#
#  Created: 14-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  14-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import core.template_engine as engine


def test_template_engine() -> None:
    class_1 = engine.ClassDefinition(name='ClassOne')
    class_1.columns.append(engine.ColumnDefinition(name='column_one',definition='int'))
    class_1.columns.append(engine.ColumnDefinition(name='column_two',definition='int'))

    class_2 = engine.ClassDefinition(name='ClassTwo')
    class_2.columns.append(engine.ColumnDefinition(name='column_one',definition='int'))
    class_2.columns.append(engine.ColumnDefinition(name='column_two',definition='int'))

    content: str = engine.create_code_file_content('model_mistral.py', [class_1, class_2])
    assert content
