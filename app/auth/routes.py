from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# models
from app.models import User, Company, db

# forms
from .forms import LoginForm, NewUserForm, UpdateUserCompanyForm, UpdateUserForm

# blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates')

# routes

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
                    flash(f'Welcome back, {username}!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(f'Incorrect password. Please try again.', 'danger')
            else:
                flash(f'No valid user with that username. Please try again.', 'danger')
                    
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
            first_name = form.first_name.data
            last_name = form.last_name.data

            # check if user exists
            user = User.query.filter_by(username=username).first()
            if user:
                flash(f'That username already exists. Please pick another name.', 'danger')
                return redirect(url_for('auth.signMeUp'))

            user = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a new user. Welcome, {username}!', 'success')
            return redirect(url_for('auth.logIn'))
    else:
            for key in form.errors:
                if key == 'email':
                    flash(form.errors[key][0], 'danger')
                elif key == 'confirm_password':
                    flash("Your passwords did not match. Please try again", 'danger')

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

        flash(f'You have successfully deleted your account.', 'success')
    return redirect(url_for('auth.logIn'))

@auth.route('/profile')
@login_required
def showProfile():
    user = User.query.filter_by(id=current_user.id).first()    
    company = Company.query.filter_by(id=user.company_id).first()
    return render_template('user_profile.html', user=user, company=company)

@auth.route('/user/update', methods=["GET","POST"])
@login_required
def updateUser():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
    form = UpdateUserForm()

    if request.method == "POST":
        if form.validate():
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            db.session.commit()

            flash('You have successfully updated your info.', 'success')
            return redirect(url_for(showProfile))
    return render_template('update_user_profile.html', form=form, user=user)

@auth.route('/user/update-company', methods=["GET","POST"])
@login_required
def updateUserCompany():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
    form = UpdateUserCompanyForm()

    if request.method == "POST":
        if form.validate():
            company_name = form.company_name.data
            company_password = form.company_password.data

            company = Company.query.filter_by(company_name=company_name).first()

            if company is None:
                flash('There is no company by that name.', 'danger')
                return redirect(url_for('auth.updateUserCompany'))
            elif company_password != company.company_password:
                flash('The company password does not match.', 'danger')
                return redirect(url_for('auth.updateUserCompany'))
            elif company_password == company.company_password:
                user.company_id = company.id
                db.session.commit()
                flash(f'You have successfully updated your company info.', 'success')
                return redirect(url_for('home'))

    return render_template('update_user_company.html', form=form, user=user)