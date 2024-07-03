#!/usr/bin/env python3
"""Game Room Routes"""
from flask import request, session, render_template, jsonify, url_for
from flask_login import login_required, current_user
from models.game_room import GameRoom
from models.user_room import UserRoom
from api.v1.views import app_views
from models import storage


@app_views.route('/game-room/<room_name>')
@login_required
def game_room(room_name):
    return render_template('game-room.html', room_name=room_name, players=[], room_creator_id=session.get('room_creator_id'))

@app_views.route('/create-room', methods=['POST'])
@login_required
def create_room():
    data = request.get_json()
    room_name = data['roomName']
    creator_id = current_user.id

    existing_rooms = storage.all(GameRoom)
    for room in existing_rooms:
        if room.name == room_name:
            return jsonify({'success': False, 'message': 'Room already exists!'}), 400

    new_room = GameRoom(name=room_name, creator_id=creator_id)
    storage.add(new_room)
    storage.save()  # Save changes to the database

    session['room_id'] = new_room.id
    session['room_creator_id'] = creator_id
    return jsonify({
        'success': True,
        'redirect_url': url_for('game_room', room_name=room_name)
    })

@app_views.route('/join-room', methods=['POST'])
@login_required
def join_room():
    data = request.get_json()
    room_name = data['roomName']
    rooms = storage.all(GameRoom)
    for room in rooms.values():
        if room.name == room_name:
            session['room_id'] = room.id
            players = get_users_in_room(room.id)
            return jsonify({
                'success': True,
                'redirect_url': url_for('game_room', room_name=room_name)
            })
    return jsonify({'success': False, 'message': 'Room does not exist!'}), 400

@app_views.route('/room_users')
def room_users():
    room_id = session.get('room_id')
    users = get_users_in_room(room_id)
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify({'users': user_list})

def get_users_in_room(room_id):
    user_rooms = storage.all(UserRoom)
    user_ids = [user_room.user_id for user_room in user_rooms.values() if user_room.room_id == room_id]
    users = [storage.get(UserRoom, user_id) for user_id in user_ids]
    return users
