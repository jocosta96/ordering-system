import pytest
from unittest.mock import MagicMock, patch
from app.adapter.outbound.repositories.sql.implementation.sql_impl import SQLRepoImpl

@pytest.fixture
def mock_db():
    with patch('app.adapter.outbound.repositories.sql.implementation.sql_impl.database.get_db') as mock_get_db:
        mock_db_instance = MagicMock()
        mock_get_db.return_value = mock_db_instance
        yield mock_db_instance

def test_try_commit_success(mock_db):
    repo = SQLRepoImpl()
    repo._database.commit = MagicMock()
    repo.try_commit()
    repo._database.commit.assert_called_once()

def test_try_commit_failure(mock_db):
    repo = SQLRepoImpl()
    repo._database.commit.side_effect = Exception('fail')
    repo._database.rollback = MagicMock()
    with pytest.raises(Exception):
        repo.try_commit()
    repo._database.rollback.assert_called_once()

def test_get_one(mock_db):
    repo = SQLRepoImpl()
    mock_entity = MagicMock()
    repo._database.query.return_value.filter_by.return_value.one.return_value = mock_entity
    result = repo.get_one(MagicMock(), {'id': 1})
    assert result == mock_entity

def test_add_one(mock_db):
    repo = SQLRepoImpl()
    entity = MagicMock()
    repo.add_one(entity)
    repo._database.add.assert_called_once_with(entity)
    repo._database.refresh.assert_called_once_with(entity)

def test_add_all(mock_db):
    repo = SQLRepoImpl()
    entities = [MagicMock(), MagicMock()]
    repo.add_all(entities)
    repo._database.add_all.assert_called_once_with(entities)
    for entity in entities:
        repo._database.refresh.assert_any_call(entity)

def test_list_all(mock_db):
    repo = SQLRepoImpl()
    repo._database.query.return_value.all.return_value = ['a', 'b']
    result = repo.list_all(MagicMock())
    assert result == ['a', 'b']

def test_list_all_with_filter_and_order(mock_db):
    repo = SQLRepoImpl()
    mock_query = repo._database.query.return_value
    mock_query.filter_by.return_value.order_by.return_value.all.return_value = ['x', 'y']
    result = repo.list_all(MagicMock(), dict_filter={'foo': 'bar'}, order_by_column='col')
    assert result == ['x', 'y']

def test_list_all_with_none_filter_and_order(mock_db):
    repo = SQLRepoImpl()
    mock_query = repo._database.query.return_value
    mock_query.all.return_value = []
    result = repo.list_all(MagicMock(), dict_filter=None, order_by_column=None)
    assert result == []

def test_update(mock_db):
    repo = SQLRepoImpl()
    repo._database.query.return_value.filter_by.return_value.update = MagicMock()
    repo.update(MagicMock(), {'field': 'value'}, {'id': 1})
    repo._database.query.return_value.filter_by.return_value.update.assert_called_once()

def test_update_commit_failure(mock_db):
    repo = SQLRepoImpl()
    repo._database.query.return_value.filter_by.return_value.update = MagicMock()
    repo.try_commit = MagicMock(side_effect=Exception('fail'))
    with pytest.raises(Exception):
        repo.update(MagicMock(), {'field': 'value'}, {'id': 1})

def test_list_all_empty_entities(mock_db):
    repo = SQLRepoImpl()
    repo._database.query.return_value.all.return_value = []
    result = repo.list_all(MagicMock())
    assert result == []

def test_add_all_empty_list(mock_db):
    repo = SQLRepoImpl()
    repo._database.add_all = MagicMock()
    repo._database.refresh = MagicMock()
    repo.add_all([])
    repo._database.add_all.assert_called_once_with([])
    repo._database.refresh.assert_not_called()

def test_get_one_not_found(mock_db):
    repo = SQLRepoImpl()
    repo._database.query.return_value.filter_by.return_value.one.side_effect = Exception('not found')
    with pytest.raises(Exception):
        repo.get_one(MagicMock(), {'id': 999})
