from flask import Blueprint, request, session, render_template
from flask_socketio import join_room, leave_room, emit
from models import db, Room, Question, UserRoom
from api.v1.app import socketio

bp = Blueprint('game_room', __name__)

@bp.route('/create_room', methods=['POST'])
def create_room():
    room_name = request.form['room_name']
    created_by = session.get('user_id')  # Assuming user sessions are set

    existing_room = Room.query.filter_by(name=room_name).first()
    if existing_room:
        return 'Room already exists!', 400

    new_room = Room(name=room_name, created_by=created_by)
    db.session.add(new_room)
    db.session.commit()

    session['room_id'] = new_room.id
    return render_template('room.html', room_name=room_name)

@bp.route('/join_room', methods=['POST'])
def join_room_route():
    room_name = request.form['room_name']
    room = Room.query.filter_by(name=room_name).first()

    if not room:
        return 'Room does not exist!', 400

    session['room_id'] = room.id
    return render_template('room.html', room_name=room_name)

@socketio.on('join')
def handle_join(data):
    room_id = session.get('room_id')
    user_id = session.get('user_id')
    username = data['username']

    join_room(room_id)
    new_user_room = UserRoom(user_id=user_id, room_id=room_id)
    db.session.add(new_user_room)
    db.session.commit()

    emit('player_joined', {'username': username}, room=room_id)

@socketio.on('leave')
def handle_leave(data):
    room_id = session.get('room_id')
    user_id = session.get('user_id')

    leave_room(room_id)
    user_room = UserRoom.query.filter_by(user_id=user_id, room_id=room_id).first()
    if user_room:
        db.session.delete(user_room)
        db.session.commit()

    emit('player_left', {'username': data['username']}, room=room_id)

@socketio.on('add_question')
def handle_add_question(data):
    room_id = session.get('room_id')
    question_text = data['question']

    new_question = Question(room_id=room_id, question_text=question_text)
    db.session.add(new_question)
    db.session.commit()

    emit('question_added', {'question': question_text}, room=room_id)

@socketio.on('start_game')
def handle_start_game(data):
    room_id = session.get('room_id')
    questions = Question.query.filter_by(room_id=room_id).all()
    question_texts = [q.question_text for q in questions]
    emit('game_started', {'questions': question_texts}, room=room_id)

def get_users_in_room(room_id):
    user_rooms = UserRoom.query.filter_by(room_id=room_id).all()
    user_ids = [user_room.user_id for user_room in user_rooms]
    users = User.query.filter(User.id.in_(user_ids)).all()
    return users

@bp.route('/room_users')
def room_users():
    room_id = session.get('room_id')
    users = get_users_in_room(room_id)
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return {'users': user_list}
