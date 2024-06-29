#!/usr/bin/env python3
"""User Model"""
from models.base_model import BaseModel
from sqlachemy import Column, String, relationship
from hashlib import md5


class User(BaseModel):
    """Representation of a user """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    user_name = Column(String(128), nullable=True)


    def __init__(self):
        """Initialization of User"""
        super().__init__()

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
