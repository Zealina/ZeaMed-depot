#!/usr/bin/env python3
"""Game Room Events"""
from flask import session, request
from flask_socketio import join_room, leave_room, emit
from flask_login import current_user
from models.user_room import UserRoom
from models.question import Question
from models.chat_message import ChatMessage
from api.v1.extension import socketio
from models import storage
from threading import Timer
from time import sleep

# ------------------------------
# Chat-related Events
# ------------------------------

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

@socketio.on('chat_history')
def handle_chat_history(data):
    print('Chat History Got Called')
    room_id = session.get('room_id')

    # Fetch all ChatMessage instances for the given room_id
    chat_history = storage.all(ChatMessage)
    filtered_history = [msg for msg in chat_history if msg.room_id == room_id]

    history_data = [{'username': msg.username, 'message': msg.message} for msg in filtered_history]
    print("History Data: ", history_data)

    emit('history_loaded', {'history': history_data}, to=request.sid)

@socketio.on('new_message')
def handle_new_message(data):
    room_id = session.get('room_id')
    username = data.get('username')  # Assuming username is passed from client
    message_text = data.get('message')

    # Create a new ChatMessage instance
    new_message = ChatMessage(room_id=room_id, username=username, message=message_text)
    storage.add(new_message)
    storage.save()  # Save message to the database

    # Broadcast the new message to all clients in the room
    emit('message_sent', {'username': username, 'message': message_text}, room=room_id)

# ------------------------------
# Other Game-related Events
# ------------------------------

@socketio.on('add_question')
def handle_add_question(data):
    room_id = session.get('room_id')
    text = data['question']
    options = data['options']
    correct_option_index = data['correct_option_index']

    new_question = Question(room_id=room_id, text=text, options=options, correct_option_index=correct_option_index)
    print(new_question.to_dict())
    storage.add(new_question)
    storage.save()  # Save changes to the database
    question_list = storage.all(Question)

    count = 0
    for question in question_list:
        if question.room_id == room_id:
            count += 1

    emit('question_added', {'count': count}, room=room_id)

#------------------------------------
# Game Logic
#------------------------------------

@socketio.on('start_game')
def handle_start_game(data):
    room_id = session.get('room_id')
    username = session.get('username')

    if is_creator(username, room_id):
        emit('game_in_progress')
        return

    questions_list = storage.all(Question)
    questions = [question for question in questions_list if question.room_id == room_id]

    if not questions:
        emit('error', {'message': 'No questions available'}, room=room_id)
        return

    question_index = 0
    scores = {player: 0 for player in get_players_in_room(room_id)}
    question_timer = None

    def send_next_question():
        nonlocal question_index, question_timer

        if question_index >= len(questions):
            emit('game_over', {'scores': scores}, room=room_id)
            return

        current_question = questions[question_index]
        question_data = {
            'question': current_question.question_text,
            'options': current_question.options.split(',,')
        }

        emit('next_question', question_data, room=room_id)

        if question_timer:
            question_timer.cancel()
        question_timer = Timer(30.0, timeout_next_question)
        question_timer.start()

    def timeout_next_question():
        nonlocal question_index
        print(f'Timeout for question {question_index + 1}')

        question_index += 1
        send_next_question()

    @socketio.on('answer_question')
    def handle_answer_question(answer_data):
        nonlocal question_index, question_timer
        player = session.get('username')
        answer = answer_data['answer']

        if player not in scores:
            return

        current_question = questions[question_index]

        if answer == current_question.options.split(',,')[current_question.correct_option_index]:
            scores[player] += 1

        question_index += 1
        print(scores)
        send_next_question()

    send_next_question()

def get_players_in_room(room_id):
    players_id_list = storage.all(UserRoom)
    room_players = [player_id for player_id in players_id_list if player_id.room_id == room_id]
    players = [storage.get(User, player_id).username for player_id in room_players]
    return players

def is_creator(username, room_id):
    room = storage.get(Room, room_id)
    return room.creator_username == username
