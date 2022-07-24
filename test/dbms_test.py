# *******************************************************************************************
#  File:  dbms_test.py
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

__all__ = []

import attrs
import pytest
import hi_henry.src.dbms as dbms
import hi_henry.src.model as model
import hi_henry.src.errors as errors


class TestMapsTable:
    def test_insert(self, database_file_name, sample_data_map_1) -> None:
        db = dbms.MapStore(database_file_name)
        rec_id = db.insert(sample_data_map_1)
        assert rec_id >= 1

    def test_insert_duplicate(self, database_file_name, sample_data_map_1) -> None:
        db = dbms.MapStore(database_file_name)
        rec_id = db.insert(sample_data_map_1)
        assert rec_id >= 1

        with pytest.raises(errors.DuplicateRecordError) as e:
            db.insert(sample_data_map_1)

        assert "A Data Map with the name" in str(e)

    def test_get(self, database_file_name, sample_data_map_1, sample_data_map_2) -> None:
        db = dbms.MapStore(database_file_name)
        rec_id = db.insert(sample_data_map_1)
        assert rec_id >= 1

        rec_id = db.insert(sample_data_map_2)
        assert rec_id >= 2

        record = db.get('SQLite', 'Standard')
        assert record
        assert record.name == 'SQLite_To_Standard'
        assert record.from_type == 'SQLite'
        assert record.to_type == 'Standard'

    def test_get_none(self, database_file_name) -> None:
        db = dbms.MapStore(database_file_name)
        record = db.get('SQLite', 'Standard')
        assert record is None


class TestProjectsTable:
    def test_insert(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)
        record = model.Project('Project 1', model.DatabaseType.MySQL, model.DtoType.Attrs,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        rec_id = db.insert(record)

        assert rec_id >= 1
        assert database_file_name.exists()

    def test_insert_duplicate(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)
        record = model.Project('Project 1', model.DatabaseType.MySQL, model.DtoType.Attrs,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        rec_id = db.insert(record)

        assert rec_id >= 1
        assert database_file_name.exists()

        with pytest.raises(errors.DuplicateRecordError) as e:
            db.insert(record)
        assert record.name in str(e)

    def test_get(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)
        record = model.Project('Project 1', model.DatabaseType.MySQL, model.DtoType.Attrs,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        rec_id = db.insert(record)

        assert rec_id >= 1
        assert database_file_name.exists()

        new_record = db.get(record.name)
        assert new_record

        assert record.name == new_record.name
        assert record.dbms == new_record.dbms
        assert record.dto == new_record.dto
        assert record.database == new_record.database
        assert record.user == new_record.user
        assert record.password == new_record.password
        assert record.host == new_record.host
        assert record.port == new_record.port

    def test_get_project_none(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)
        record = db.get("Project 10")
        assert record is None

    def test_update(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)
        record = model.Project('Project 1', model.DatabaseType.MySQL, model.DtoType.Attrs,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        rec_id = db.insert(record)

        assert rec_id >= 1
        assert database_file_name.exists()

        # noinspection PyDataclass
        update_record = attrs.evolve(record, dbms=model.DatabaseType.PostgreSQL, dto=model.DtoType.DataClasses)

        db.update(update_record)
        update_record = db.get(update_record.name)

        assert record.name == update_record.name
        assert record.dbms != update_record.dbms
        assert record.dto != update_record.dto

    def test_update_none(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)
        record = model.Project('Project 1', model.DatabaseType.MySQL, model.DtoType.Attrs,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)

        with pytest.raises(errors.RecordNotFoundError) as e:
            db.update(record)
        assert record.name in str(e)

    def test_get_projects(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)

        record = model.Project('Project 1', model.DatabaseType.MySQL, model.DtoType.Attrs,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        db.insert(record)

        record = model.Project('Project 2', model.DatabaseType.PostgreSQL, model.DtoType.DataClasses,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        db.insert(record)

        record = model.Project('Project 3', model.DatabaseType.SQLite, model.DtoType.Pydantic,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        db.insert(record)

        record = model.Project('Project 4', model.DatabaseType.MySQL, model.DtoType.DataClasses,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        db.insert(record)

        record = model.Project('Project 5', model.DatabaseType.SQLite, model.DtoType.Attrs,
                               'joey_data', 'joe', 'letjoeyin', '1.0.0.127', 5432)
        db.insert(record)

        rows = db.all()
        assert len(rows) == 5

    def test_get_projects_none(self, database_file_name) -> None:
        db = dbms.ProjectStore(database_file_name)

        rows = db.all()
        assert rows is None
