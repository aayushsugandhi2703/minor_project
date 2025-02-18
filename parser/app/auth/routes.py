from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required
from app.forms import RegisterForm, LoginForm
from app.models import User, session_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

auth_bp = Blueprint('auth', __name__)

# initializing the limiter with default limits
limiter = Limiter(key_func=get_remote_address, default_limits=["10 per minute"])

#this route is for registering a new user
@limiter.limit("5 per minute")
@auth_bp.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data ).first()
        if user:
            return redirect(url_for('auth.signup'))
        else:
            new_user = User( name = form.name.data, 
                            email = form.email.data, 
                            password = generate_password_hash(form.password.data, method='sha256') )
            current_app.logger.info(f'New user {new_user.email} created at {new_user.created_at}')
            session_db.add(new_user)
            session_db.commit()
            return redirect(url_for('auth.signin'))
    return render_template('register.html', form=form)

# This route is for logging in the user
@limiter.limit("5 per minute")
@auth_bp.route('/login', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            current_app.logger.info(f'User {form.email.data} logged in at ')
            return redirect(url_for('service.home'))
        else:
            current_app.logger.info(f'Failed login attempt for {form.email.data}')
            return redirect(url_for('auth.signin'))
    return render_template('login.html', form=form)

# This route is for logging out the user
@login_required
@auth_bp.route('/logout')
def signout():
    logout_user()
    session.clear()
    current_app.logger.info(f'User logged out')
    return redirect(url_for('auth.signin'))