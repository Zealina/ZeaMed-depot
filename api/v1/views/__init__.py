#!/usr/bin/env python3
"""Initialize blueprint for all views"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.auth import *
from api.v1.views.dashboard import *
from api.v1.views.game_room import *
from api.v1.views.question import *
