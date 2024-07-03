#!/usr/bin/env python3
"""Association Model for GameRoom with users"""

from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel

class UserRoom(BaseModel):
    """Table That Associates Users with user room"""
    __tablename__ = 'user_rooms'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    room_id = Column(String(60), ForeignKey('game_rooms.id'), nullable=False)
