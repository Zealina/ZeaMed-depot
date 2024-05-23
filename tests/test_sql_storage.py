import unittest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.engine.sql_storage import SQLStorage
from models.question import Base, Question

class TestSQLStorage(unittest.TestCase):

    @patch('models.engine.sql_storage.getenv')
    def setUp(self, mock_getenv):
        """Set up an in-memory SQLite database for testing."""
        mock_getenv.side_effect = lambda x: {
            'ZMD_USERNAME': 'test_user',
            'ZMD_PASSWD': 'test_pass',
            'ZMD_HOST': 'localhost',
            'ZMD_DBNAME': 'test_db'
        }.get(x)
        self.storage = SQLStorage()
        self.storage._SQLStorage__engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.storage._SQLStorage__engine)
        Session = sessionmaker(bind=self.storage._SQLStorage__engine)
        self.storage._SQLStorage__session = Session()

    def tearDown(self):
        """Tear down the in-memory SQLite database."""
        Base.metadata.drop_all(self.storage._SQLStorage__engine)
        self.storage._SQLStorage__session.close()

    def test_initialization(self):
        """Test if the storage is initialized correctly."""
        self.assertIsNotNone(self.storage._SQLStorage__engine)

    def test_reload(self):
        """Test if reload creates a session."""
        self.storage.reload()
        self.assertIsNotNone(self.storage._SQLStorage__session)

    def test_all(self):
        """Test retrieving all objects from the database."""
        self.storage.reload()
        all_questions = self.storage.all(Question)
        self.assertEqual(len(all_questions), 0)

    def test_new_and_save(self):
        """Test adding and saving a new object."""
        self.storage.reload()
        new_question = Question(question="Test question")
        self.storage.new(new_question)
        self.storage.save()
        self.assertEqual(len(self.storage.all(Question)), 1)

    def test_delete(self):
        """Test deleting an object."""
        self.storage.reload()
        new_question = Question(question="Test question")
        self.storage.new(new_question)
        self.storage.save()
        self.storage.delete(new_question)
        self.storage.save()
        self.assertEqual(len(self.storage.all(Question)), 0)

    def test_get(self):
        """Test getting an object by id."""
        self.storage.reload()
        new_question = Question(id="1", question="Test question")
        self.storage.new(new_question)
        self.storage.save()
        obj = self.storage.get("1", Question)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.question, "Test question")

    def test_count(self):
        """Test counting the number of objects in the database."""
        self.storage.reload()
        count = self.storage.count(Question)
        self.assertEqual(count, 0)
        new_question = Question(question="Test question")
        self.storage.new(new_question)
        self.storage.save()
        count = self.storage.count(Question)
        self.assertEqual(count, 1)

    def test_close(self):
        """Test closing the session."""
        self.storage.reload()
        self.storage.close()
        self.assertRaises(Exception, self.storage._SQLStorage__session.query, Question)

if __name__ == '__main__':
    unittest.main()
