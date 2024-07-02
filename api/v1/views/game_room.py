#!/usr/bin/env python3
"""Game Room Management"""
from flask import request, session, render_template, jsonify
from flask_socketio import join_room, leave_room, emit
from flask_login import login_required, current_user
from models.game_room import GameRoom
from models.question import Question
from models.user_room import UserRoom
from api.v1.app import socketio
from api.v1.views import app_views
from models import storage

@app_views.route('/game_room')
@login_requid
def index():
    render_template('game-room.html')

@app_views.route('/create_room', methods=['POST'])
@login_required
def create_room():
    room_name = request.form['room_name']
    creator_id = current_user.id

    existing_rooms = storage.all(GameRoom)
    for room in existing_rooms.values():
        if room.name == room_name:
            return 'Room already exists!', 400

    new_room = GameRoom(name=room_name, creator_id=creator_id)
    storage.add(new_room)
    storage.save()  # Save changes to the database

    session['room_id'] = new_room.id
    session['room_creator_id'] = creator_id
    return render_template('game-room.html', room_name=room_name, players=[], room_creator_id=creator_id)

@app_views.route('/join_room', methods=['POST'])
@login_required
def join_room_route():
    room_name = request.form['room_name']
    rooms = storage.all(GameRoom)
    for room in rooms.values():
        if room.name == room_name:
            session['room_id'] = room.id
            players = get_users_in_room(room.id)
            return render_template('game-room.html', room_name=room_name, players=players, room_creator_id=room.creator_id)
    return 'Room does not exist!', 400

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

def get_users_in_room(room_id):
    user_rooms = storage.all(UserRoom)
    user_ids = [user_room.user_id for user_room in user_rooms.values() if user_room.room_id == room_id]
    users = [storage.get(UserRoom, user_id) for user_id in user_ids]
    return users

@app_views.route('/room_users')
def room_users():
    room_id = session.get('room_id')
    users = get_users_in_room(room_id)
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify({'users': user_list})
