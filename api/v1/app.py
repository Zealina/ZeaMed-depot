#!/usr/bin/env python3
"""authentication endpoints"""

from flask import Flask
from os import getenv
from flask_login import LoginManager
from models.user import User
from api.v1.views import app_views
from models import storage


def create_app():
    app = Flask(__name__)

    app.secret_key = getenv("ZEAMED_SECRET_KEY")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return storage.get(User, user_id)

    app.register_blueprint(app_views)
    return app
