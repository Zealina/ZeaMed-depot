from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel

class ChatMessage(BaseModel):
    __tablename__ = 'chat_messages'

    room_id = Column(String(60), ForeignKey('game_rooms.id', ondelete='CASCADE'), nullable=False)
    username = Column(String(128), nullable=False)
    message = Column(String(1024), nullable=False)
