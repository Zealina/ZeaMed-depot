#!/usr/bin/env python3

from flask import render_template
from flask_login import login_required, current_user
from api.v1.views import app_views

@app_views.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user)
