#!/usr/bin/env python3
"""Questions Model for Game Room"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Question(BaseModel):
    """Model for storing Multiple Choice Questions (MCQs)"""

    __tablename__ = 'questions'

    text = Column(String(255), nullable=False)
    options = Column(String(1024), nullable=False)
    correct_option_index = Column(String(10), nullable=False)
    game_room_id = Column(String(60), ForeignKey('game_rooms.id'))

    game_room = relationship('GameRoom', back_populates='questions')

    def __init__(self, text, options, correct_option_index, game_room=None, **kwargs):
        self.text = text
        self.options = '|'.join(options)
        self.correct_option_index = correct_option_index
        self.game_room = game_room
        super().__init__(**kwargs)

    def to_dict(self, save_fs=None):
        data = super().to_dict(save_fs)
        data['options'] = self.options.split('|')
        return data
