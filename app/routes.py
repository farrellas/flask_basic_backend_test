from flask_login import current_user, login_fresh, login_required
from app import app
from flask import render_template, redirect, url_for

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/main')
@login_required
def main():
    return render_template('main.html')