from flask import Blueprint, render_template, redirect, url_for, flash, make_response, session,current_app
from flask_jwt_extended import create_access_token, create_refresh_token    
from app.Models.models import User, Session
from app.Forms.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_user, logout_user, login_required, current_user
import time
from prometheus_client import Histogram

api_bp = Blueprint('api', __name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["5 per minute"])

Request_latency_login = Histogram('login_latency', 'Histogram tracking login latency', buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10])
Request_latency_register = Histogram('fregister_latency', 'Histogram tracking register latency', buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10])

# This function will redirect the user to the login page
@api_bp.route('/')
def index():
    return redirect(url_for('api.Login'))

# This function and route is for the user to login 
@api_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def Login():
    with Request_latency_login.time():
        login_form = LoginForm()
        form = RegisterForm()

        if login_form.validate_on_submit():
            user = Session.query(User).filter_by(username=login_form.username.data).first()
            if user and check_password_hash(user.password, login_form.password.data):
                current_app.logger.info(f"User {login_form.username.data} logged in successfully")

                session['user_id'] = user.id
                session['username'] = user.username
                login_user(user)
                session['email'] = user.email   
                

                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                response = make_response(redirect(url_for('service.Upload_Parse')))  
                response.set_cookie('access_token_cookie', access_token, httponly=True)
                response.set_cookie('refresh_token_cookie', refresh_token, httponly=True)

                return response 
            else:
                current_app.logger.info(f"User {login_form.username.data} login unsuccessfully or not a user")

    return render_template('auth.html', login_form=login_form, form=form)

# This function and route is for the user to register
@api_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def Register():
    with Request_latency_register.time():

        login_form = LoginForm()
        form = RegisterForm()
        if form.validate_on_submit():
            if Session.query(User).filter_by(username=form.username.data).first():
                flash('Username already exists')
                return redirect(url_for('api.Register'))
        # If the form is submitted and validated, the user will be redirected to the login page
        if form.validate_on_submit():
            passcode = generate_password_hash(form.password.data)   
            new_user = User( name=form.name.data, email=form.email.data, organization=form.organization.data, phone=form.phone.data, username=form.username.data, password=passcode)
            Session.add(new_user)
            Session.commit()
            current_app.logger.info(f"User {form.username.data} signup successfully")
            return redirect(url_for('api.Login'))
        else:
            Session.rollback()
            current_app.logger.info(f"User {form.username.data} signup unsuccessfully")
    
    return render_template('auth.html', form=form, login_form=login_form)

@api_bp.route('/profile', methods=['GET'])
@login_required
def Profile():
    user = current_user
    current_app.logger.info(f"User {session['username']} profile accessed successfully")
    return render_template('profile.html', user=user)

# This function and route is for the user to logout
@api_bp.route('/logout', methods=['GET'])  
@login_required
def Logout():

    response = make_response(redirect(url_for('api.Login')))
    response.delete_cookie('access_token_cookie')  
    response.delete_cookie('refresh_token_cookie') 
    logout_user()
    session.clear()
    current_app.logger.info(f"User logout successfully")

    return response
