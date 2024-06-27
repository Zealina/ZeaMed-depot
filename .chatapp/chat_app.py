#!/usr/bin/env python3
"""Realtime Multiplayer Trivia Game API"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    """Index page"""
    return render_template('chat.html')

@socketio.on("connect")
def test_connect():
    """Check if connection has been established"""
    print("Connection is successful!")

@socketio.on('user_join')
def handle_user_join(username):
    """Add user to chat"""
    print(f"User: {username} joined")

@socketio.on('new_message')
def handle_new_message(msg):
    """Handle new message"""
    print(f'Message: {msg}')
    emit("chat", {"message": msg}, broadcast=True)



@socketio.on("disconnect")
def test_disconnect():
    """Test disconnection to client"""
    print("Client Disconnected")


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
