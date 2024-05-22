#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.question import Base, Question
from os import getenv


class SQLStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        ZMD_USERNAME = getenv('ZMD_USERNAME')
        ZMD_PASSWD = getenv('ZMD_PASSWD')
        ZMD_HOST = getenv('ZMD_HOST')
        ZMD_DBNAME = getenv('ZMD_DBNAME')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(ZMD_USERNAME,
                                             ZMD_PASSWD,
                                             ZMD_HOST,
                                             ZMD_DBNAME))

    def all(self, cls=None):
        """query on the current database session"""
        pass

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        pass

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        pass
