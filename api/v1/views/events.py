#!/usr/bin/env python3
"""Game Room Events"""
from flask import session
from flask_socketio import join_room, leave_room, emit
from flask_login import current_user
from models.user_room import UserRoom
from models.question import Question
from api.v1.extension import socketio
from models import storage

@socketio.on('join')
def handle_join(data):
    room_id = session.get('room_id')
    user_id = current_user.id
    username = data['username']

    join_room(room_id)
    new_user_room = UserRoom(user_id=user_id, room_id=room_id)
    storage.add(new_user_room)
    storage.save()  # Save changes to the database

    emit('player_joined', {'username': username}, room=room_id)
    emit('chat_message', {'message': f'{username} has joined the game.'}, room=room_id)

@socketio.on('leave')
def handle_leave(data):
    room_id = session.get('room_id')
    user_id = current_user.id

    leave_room(room_id)
    user_rooms = storage.all(UserRoom)
    for user_room in user_rooms.values():
        if user_room.room_id == room_id and user_room.user_id == user_id:
            storage.delete(user_room)
            storage.save()  # Save changes to the database
    emit('player_left', {'username': data['username']}, room=room_id)

@socketio.on('add_question')
def handle_add_question(data):
    room_id = session.get('room_id')
    question_text = data['question']

    new_question = Question(room_id=room_id, question_text=question_text)
    storage.add(new_question)
    storage.save()  # Save changes to the database

    emit('question_added', {'question': question_text}, room=room_id)

@socketio.on('start_game')
def handle_start_game(data):
    room_id = session.get('room_id')
    questions = storage.query(Question).filter_by(room_id=room_id).all()
    question_texts = [q.question_text for q in questions]
    emit('game_started', {'questions': question_texts}, room=room_id)
