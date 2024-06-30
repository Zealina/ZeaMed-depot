#!/usr/bin/env python3
"""User Model"""
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel, UserMixin):
    """Representation of a user """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    username = Column(String(128), nullable=True)

    def __init__(self, **kwargs):
        """Initialization of User"""
        super().__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
