#!/usr/bin/env python3
"""Questions Model for Game Room"""

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Question(BaseModel):
    """Model for storing Multiple Choice Questions (MCQs)"""

    __tablename__ = 'questions'

    text = Column(String(255), nullable=False)
    options = Column(String(1024), nullable=False)
    correct_option_index = Column(Integer, nullable=False)
    room_id = Column(String(60), ForeignKey('game_rooms.id'))


    def to_dict(self):
        data = super().to_dict()
        data['options'] = self.options.split(',,')
        return data
