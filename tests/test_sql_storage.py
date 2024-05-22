import unittest
from models.engine.sql_storage import SQLStorage
from models.question import Question
from unittest.mock import patch

class TestSQLStorage(unittest.TestCase):

    @patch('models.engine.sql_storage.create_engine')
    def test_init(self, mock_create_engine):
        storage = SQLStorage()
        mock_create_engine.assert_called_once()

    @patch('models.engine.sql_storage.SQLStorage.__session')
    def test_all(self, mock_session):
        storage = SQLStorage()
        storage.all()
        mock_session.query.assert_called_once()

    @patch('models.engine.sql_storage.SQLStorage.__session')
    def test_new(self, mock_session):
        storage = SQLStorage()
        q = Question(question="What is the capital of France?")
        storage.new(q)
        mock_session.add.assert_called_once_with(q)

    @patch('models.engine.sql_storage.SQLStorage.__session')
    def test_save(self, mock_session):
        storage = SQLStorage()
        storage.save()
        mock_session.commit.assert_called_once()

    @patch('models.engine.sql_storage.SQLStorage.__session')
    def test_delete(self, mock_session):
        storage = SQLStorage()
        q = Question(question="What is the capital of France?")
        storage.delete(q)
        mock_session.delete.assert_called_once_with(q)

    @patch('models.engine.sql_storage.SQLStorage.__session')
    def test_reload(self, mock_session):
        storage = SQLStorage()
        storage.reload()
        self.assertTrue(mock_session)

    @patch('models.engine.sql_storage.SQLStorage.__session')
    def test_get(self, mock_session):
        storage = SQLStorage()
        storage.get('123')
        mock_session.query.assert_called_once_with(Question)

    @patch('models.engine.sql_storage.SQLStorage.__session')
    def test_count(self, mock_session):
        storage = SQLStorage()
        storage.count()
        mock_session.query.assert_called_once_with(Question)

if __name__ == '__main__':
    unittest.main()
