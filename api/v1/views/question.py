# api/v1/views/game.py

from flask import request, jsonify, render_template
from flask_login import login_required
from models import storage
from models.game_room import GameRoom
from models.question import Question
from api.v1.views import app_views


@app_views.route('/questions', methods=['GET'])
def list_questions():
    questions = storage.all(Question)
    return jsonify([question.to_dict() for question in questions])

@app_views.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    question_text = data['question_text']
    answer = data['answer']
    # Additional attributes as needed
    new_question = Question(question_text=question_text, answer=answer)
    storage.add(new_question)
    return jsonify({"message": "Question created", "id": new_question.id}), 201
