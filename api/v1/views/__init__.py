#!/usr/bin/env python3
"""Initialize blueprint for all views"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')