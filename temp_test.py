import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

# Example User model for testing
class User(BaseModel):
    """User class inheriting from BaseModel"""
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        """Initialization of the User class"""
        super().__init__(*args, **kwargs)

# Fixture to set up the database engine and session
@pytest.fixture(scope='module')
def setup_database():
    # Create an in-memory SQLite database
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_user(setup_database):
    session = setup_database
    # Create a new user instance
    new_user = User(name="John Doe", email="john.doe@example.com")
    session.add(new_user)
    session.commit()
    
    # Retrieve the user from the database
    retrieved_user = session.query(User).filter_by(email="john.doe@example.com").first()
    
    print("Created user:", new_user)
    print("Retrieved user:", retrieved_user)
    
    assert retrieved_user is not None
    assert retrieved_user.name == "John Doe"
    assert retrieved_user.email == "john.doe@example.com"
    assert isinstance(retrieved_user.created_at, datetime)
    assert isinstance(retrieved_user.updated_at, datetime)

def test_to_dict_method(setup_database):
    session = setup_database
    new_user = User(name="Jane Doe", email="jane.doe@example.com")
    user_dict = new_user.to_dict()
    
    print("User to_dict output:", user_dict)
    
    assert user_dict["name"] == "Jane Doe"
    assert user_dict["email"] == "jane.doe@example.com"
    assert "__class__" in user_dict
    assert user_dict["__class__"] == "User"

def test_save_method(setup_database):
    session = setup_database
    new_user = User(name="Alice", email="alice@example.com")
    session.add(new_user)
    session.commit()
    
    # Modify the user and save
    new_user.name = "Alice Updated"
    new_user.save()
    session.commit()
    
    updated_user = session.query(User).filter_by(email="alice@example.com").first()
    
    print("Updated user:", updated_user)
    
    assert updated_user.name == "Alice Updated"
    assert updated_user.updated_at > updated_user.created_at

def test_delete_method(setup_database):
    session = setup_database
    new_user = User(name="Bob", email="bob@example.com")
    session.add(new_user)
    session.commit()
    
    # Delete the user
    session.delete(new_user)
    session.commit()
    
    deleted_user = session.query(User).filter_by(email="bob@example.com").first()
    
    print("Deleted user:", deleted_user)
    
    assert deleted_user is None
