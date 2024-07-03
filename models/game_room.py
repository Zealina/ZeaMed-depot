from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.chat_message import ChatMessage  # Ensure correct import

class GameRoom(BaseModel):
    """Model for representing a game room"""

    __tablename__ = 'game_rooms'

    name = Column(String(255), nullable=False)
    creator_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    messages = relationship('ChatMessage', backref='game_room', cascade='all, delete-orphan')

    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)
