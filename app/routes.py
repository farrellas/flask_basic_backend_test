from flask_login import current_user
from app import app
from flask import render_template, redirect, url_for

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('logs.userLogs'))
    return render_template('index.html')