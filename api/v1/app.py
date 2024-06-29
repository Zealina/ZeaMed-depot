#!/usr/bin/env python3
"""authentication endpoints"""

from flask import Flask, render_template
from os import getenv

app = Flask(__name__)

@app.route('/')
def index():
    return"Welcome to my App"

@app.route('/test')
def test_html():
    html = getenv('html')
    return render_template(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
