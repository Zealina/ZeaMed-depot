#!/usr/bin/env python3
"""Test the questions and Game room models"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.game_room import GameRoom
from models.question import Question

# Database setup
ZEAMED_MYSQL_USER = os.getenv('ZEAMED_MYSQL_USER', 'zeamed_test')
ZEAMED_MYSQL_PWD = os.getenv('ZEAMED_MYSQL_PWD', 'zeamed_test_pwd')
ZEAMED_MYSQL_HOST = os.getenv('ZEAMED_MYSQL_HOST', 'localhost')
ZEAMED_MYSQL_DB = os.getenv('ZEAMED_MYSQL_DB', 'zeamed_test_db')
ZEAMED_MYSQL_ENV = os.getenv('ZEAMED_MYSQL_ENV', 'test')

engine = create_engine(f'mysql+pymysql://{ZEAMED_MYSQL_USER}:{ZEAMED_MYSQL_PWD}@{ZEAMED_MYSQL_HOST}/{ZEAMED_MYSQL_DB}')
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
session = Session()

# Creating a new user (creator)
creator = User(email="creator@example.com", password="password", firstname="John", lastname="Doe", username="johndoe")
session.add(creator)
session.commit()

# Creating a game room
game_room = GameRoom(name="Trivia Room 1", creator=creator)
session.add(game_room)
session.commit()

# Adding questions to the game room
question1 = Question(text="What is the capital of France?", options=["Paris", "London", "Berlin", "Rome"], correct_option_index="0", game_room=game_room)
question2 = Question(text="Which planet is known as the Red Planet?", options=["Earth", "Mars", "Jupiter", "Saturn"], correct_option_index="1", game_room=game_room)
session.add(question1)
session.add(question2)
session.commit()

# Print game room and questions
print("Game Room Created:")
print(game_room)
print("\nQuestions Added:")
print(question1)
print(question2)

# Start the game
game_room.game_started = True
session.commit()

print("\nGame Started:", game_room.game_started)

# Deleting the game room (which will also delete associated questions)
session.delete(game_room)
session.commit()

print("\nGame Room and associated questions deleted.")
