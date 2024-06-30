# api/v1/views/game.py

from flask import request, jsonify, render_template
from flask_login import login_required
from models import storage
from models.game_room import GameRoom
from models.question import Question
from api.v1.views import app_views

# Game Rooms Endpoints

@app_views.route('/gamerooms', methods=['GET'])
def list_game_rooms():
    game_rooms = storage.all(GameRoom)
    return jsonify([game_room.to_dict() for game_room in game_rooms])

@app_views.route('/gamerooms', methods=['POST'])
def create_game_room():
    data = request.get_json()
    room_name = data['room_name']
    # Additional attributes as needed
    new_game_room = GameRoom(room_name=room_name)
    storage.add(new_game_room)
    return jsonify({"message": "Game room created", "id": new_game_room.id}), 201
