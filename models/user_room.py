#!/usr/bin/env python3
"""Association Model for GameRoom with users"""

from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel

class UserRoom(BaseModel):
    """Table That Associates Users with user room"""
    __tablename__ = 'user_rooms'

    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    room_id = Column(String, ForeignKey('room.id'), nullable=False)
