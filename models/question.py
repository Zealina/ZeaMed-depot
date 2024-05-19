#!/usr/bin/env python3
"""Questions Module contains the question class and all related functions"""

from datetime import datetime
import typing
from uuid import uuid4


class Question:
    """Class to create questions object"""
    def __init__(self, question, answer=None, options=None, verified=False,
            posting=None, pq=True, explanation=None, **kwargs) -> None:
        """Initialize the questions class"""
        self.id = str(uuid4())
        self.question = question
        self.options = options if options else {"A": True, "B": False}
        self.answer = answer
        self.posting = posting
        self.pq = pq
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', self.created_at)
        self.explanation = explanation
        self.verified = verified
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """Convert instance to dictionary"""
        my_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                my_dict[key] = str(value)
            else:
                my_dict[key] = value
        return my_dict

    def update(self, **kwargs) -> None:
        """Update the options of a question"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now()

    def __repr__(self):
        """String Reprsentation of the instance"""
        return f"[({self.id}) - ({self.posting})] - {self.question}"
