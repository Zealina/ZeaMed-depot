#!/usr/bin/env python3
"""DB storage for App"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv

class Storage:
    """Handles the storage of models in the database."""

    __session = None
    __engine = None

    def __init__(self):
        """Create DB Engine"""
        ZEAMED_MYSQL_USER = getenv('ZEAMED_MYSQL_USER')
        ZEAMED_MYSQL_PWD = getenv('ZEAMED_MYSQL_PWD')
        ZEAMED_MYSQL_HOST = getenv('ZEAMED_MYSQL_HOST')
        ZEAMED_MYSQL_DB = getenv('ZEAMED_MYSQL_DB')
        ZEAMED_ENV = getenv('ZEAMED_ENV')
        self.__engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.
                                      format(ZEAMED_MYSQL_USER,
                                             ZEAMED_MYSQL_PWD,
                                             ZEAMED_MYSQL_HOST,
                                             ZEAMED_MYSQL_DB))
        if ZEAMED_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def add(self, obj):
        """Add a new object to the database."""
        self.__session.add(obj)
        self.__session.commit()

    def get(self, cls, id):
        """Retrieve an object by its ID."""
        return self.__session.query(cls).get(id)

    def delete(self, obj):
        """Delete an object from the database."""
        self.__session.delete(obj)
        self.__session.commit()

    def update(self, obj):
        """Update an existing object in the database."""
        self.__session.merge(obj)
        self.__session.commit()

    def all(self, cls):
        """Retrieve all objects of a given class."""
        return self.__session.query(cls).all()

    def close(self):
        """Close the self.__session."""
        self.__session.close()
