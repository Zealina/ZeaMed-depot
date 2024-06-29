#!/usr/bin/env python3
"""Model for the game room"""

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class GameRoom(BaseModel):
    """Model for representing a game room"""

    __tablename__ = 'game_rooms'

    name = Column(String(255), nullable=False)
    creator_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    game_started = Column(Boolean, default=False)

    creator = relationship('User')
    questions = relationship('Question', back_populates='game_room', cascade='all, delete-orphan')

    def __init__(self, name, creator, **kwargs):
        self.name = name
        self.creator = creator
        super().__init__(**kwargs)
