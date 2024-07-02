#!/usr/bin/env python3

"""Temporary Quiz MUltiplayer app"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

questions = [
    "What is the capital of France? A) Paris B) London C) Rome D) Madrid",
    "What is 2 + 2? A) 3 B) 4 C) 5 D) 6",
]

players = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    data = message.get('data')
    if data:
        print('received message: ' + data)
    else:
        print('received message')

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('join')
def on_join(data):
    username = data.get('username')
    if username:
        players[request.sid] = username
        send_question()

@socketio.on('answer')
def on_answer(data):
    answer = data.get('answer')
    if answer:
        print(f'Player {players[request.sid]} answered: {answer}')

def send_question():
    question = choice(questions)
    for sid in players.keys():
        emit('question', {'type': 'question', 'question': question}, to=sid)

if __name__ == '__main__':
    socketio.run(app)
