from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# forms
from .forms import LoginForm, NewUserForm

# models
from app.models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/login', methods=["GET","POST"])
def logIn():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        if form.validate():
            username = form.username.data.lower()
            password = form.password.data
            remember_me = form.remember_me.data

            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=remember_me)
                    return redirect(url_for('home'))
                    
            redirect(url_for('auth.logIn'))
            
            

    return render_template('login.html', form=form)

@auth.route('/signup', methods=["GET","POST"])
def signMeUp():
    form = NewUserForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        if form.validate():
            username = form.username.data.lower()
            email = form.email.data
            password = form.password.data

            user = User(username=username, email=email, password=password)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.logIn'))

    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logIn'))

@auth.route('/delete-user', methods=["POST"])
@login_required
def deleteUser():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()

        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('auth.logIn'))