#!/usr/bin/env python3
"""Questions Module contains the question class and all related functions"""

from datetime import datetime
from uuid import uuid4
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Boolean, DateTime, ARRAY

Base = declarative_base()


class Question(Base):
    """Class to create questions object"""

    __tablename__ = 'questions'
    
    id = Column(String(36), primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    options = Column(ARRAY(Text), default=[True, False])
    verified = Column(Boolean, default=False)
    posting = Column(Text)
    pq = Column(Boolean, default=True)
    explanation = Column(Text)
    topic = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
                        DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)


    def __init__(self, question, answer=None, options=[True, False], verified=False,
                 posting=None, pq=True, explanation=None, topic=None,
                 **kwargs) -> None:
        """Initialize the questions class"""
        self.id = str(uuid4())
        self.__question = question
        self.__answer = answer
        self.__options = options
        self.__posting = posting
        self.__topic = topic
        self.__pq = pq
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', self.created_at)
        self.__explanation = explanation
        self.__verified = verified
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def question(self):
        """Getter method"""
        return self.__question

    @question.setter
    def question(self, value):
        """Setter method"""
        if value and type(value) is str:
            self.__question = value
        elif not value:
            raise ValueError("Question must be present")
        else:
            raise ValueError("Question must be a string")

    @property
    def options(self):
        """Getter method"""
        return self.__options

    @options.setter
    def options(self, value):
        """Setter method"""
        if value:
            if isinstance(value, list):
                self.__options = value
            else:
                raise ValueError("Options must be a List")
        else:
            self.__options = None
        if self.answer and value and self.answer not in value:
            self.answer = None

    @property
    def answer(self):
        """Getter method"""
        return self.__answer

    @answer.setter
    def answer(self, value):
        """Setter method"""
        if value:
            if isinstance(value, (str, int, bool)):
                self.__answer = value
            else:
                raise ValueError("Answer is invalid data ttpe")
        else:
            self.__answer = None
        if self.options and value not in self.options:
            self.options = None

    @property
    def posting(self):
        """Getter method"""
        return self.__posting

    @posting.setter
    def posting(self, text):
        """Setter method"""
        self.__posting = None
        if type(text) is str:
            self.__posting = text

    @property
    def topic(self):
        """Getter method"""
        return self.__topic

    @topic.setter
    def topic(self, text):
        """Setter method"""
        self.__topic = None
        if type(text) is str:
            self.__topic = text

    @property
    def pq(self):
        """Getter method"""
        return self.__pq

    @pq.setter
    def pq(self, value):
        """Setter method"""
        self.__pq = True
        if type(value) is bool:
            self.__pq = value

    @property
    def verified(self):
        """Getter method"""
        return self.__verified

    @verified.setter
    def verified(self, value):
        """Setter method"""
        if type(value) is bool:
            self.__verified = value
        else:
            self.__verified = False

    @property
    def explanation(self):
        """Getter method"""
        return self.__explanation

    @explanation.setter
    def explanation(self, value):
        """Setter method"""
        if type(value) is str:
            self.__explanation = value
        else:
            self.__explanation = None

    def to_dict(self):
        """Convert instance to dictionary"""
        my_dict = {}
        for key, value in self.__dict__.items():
            if key == '_sa_instance_state':
                continue
            key = key.replace('_' + self.__class__.__name__ + '__', '')
            if isinstance(value, datetime):
                my_dict[key] = str(value)
            else:
                my_dict[key] = value
        return my_dict

    def update(self, **kwargs) -> None:
        """Update the options of a question"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__updated_at = datetime.now()

    def __repr__(self):
        """String Reprsentation of the instance"""
        return (f"[({self.id}) - ({self.posting}"
                f", {self.topic})] - {self.question}")
