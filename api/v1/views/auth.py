#!/usr/bin/env python3
"""Authentication Routes"""
from flask import request, jsonify, render_template
from flask_login import login_user, logout_user, login_required
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    firstname = data['firstname']
    lastname = data['lastname']

    for user in  storage.all(User):
        if user.email == email:
            return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, email=email, firstname=firstname, lastname=lastname)
    new_user.password = password
    storage.add(new_user)
    return jsonify({"message": "Registration successful", "id": new_user.id}), 201


@app_views.route('/auth/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.get_json()
    email = data['email']
    password = data['password']

    user_list = storage.all(User)

    for user in user_list:
        if user.email == email and user.password == password:
            login_user(user)
            return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid email or password"}), 401


@app_views.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200
