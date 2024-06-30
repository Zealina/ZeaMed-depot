# app/views/auth.py
"""Authentication Routes"""
from flask import request, jsonify
from flask_login import login_user, logout_user, login_required
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    firstname = data['firstname']
    lastname = data['lastname']

    if db_session.query(User).filter_by(email=email).first() or db_session.query(User).filter_by(username=username).first():
        db_session.close()
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, email=email, firstname=firstname, lastname=lastname)
    new_user.password = password
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

    return jsonify({"message": "Registration successful"}), 201

@app_views.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    db_session = SessionLocal()
    user = db_session.query(User).filter_by(email=email).first()

    if user is None or not user.check_password(password):
        db_session.close()
        return jsonify({"message": "Invalid email or password"}), 401

    login_user(user)
    db_session.close()
    return jsonify({"message": "Login successful"}), 200

@app_views.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200
