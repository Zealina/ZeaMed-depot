#!/usr/bin/env python3
"""User Model"""
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    """Representation of a user """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)  # Update to match DB schema
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    username = Column(String(128), nullable=True)

    def __init__(self, **kwargs):
        """Initialization of User"""
        super().__init__(**kwargs)
