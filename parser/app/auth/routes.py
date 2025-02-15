from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
from app.models import User, Session
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_user, logout_user, login_required
from sqlalchemy.orm import scoped_session

# Blueprint for authentication
auth_bp = Blueprint('auth', __name__)  

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address, default_limits=["5 per minute"])

# Scoped session to ensure thread safety
db_session = scoped_session(Session)

# User Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = db_session.query(User).filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                current_app.logger.info(f"[LOGIN SUCCESS] User '{form.username.data}' logged in.")

                session['user_id'] = user.id  # Store user session
                login_user(user)  # Flask-Login session management
                
                return redirect(url_for('service_bp.fetch_save'))
            else:
                current_app.logger.warning(f"[LOGIN FAILED] Invalid login attempt for '{form.username.data}'.")
        except Exception as e:
            current_app.logger.error(f"[LOGIN ERROR] Unexpected error for '{form.username.data}': {e}")
        finally:
            db_session.remove()  # Ensure session is properly closed

    return render_template('Login.html', form=form)


# User Registration Route
@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def Register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data)  
            user = User(username=form.username.data, password=hashed_password)

            db_session.add(user)
            db_session.commit()
            current_app.logger.info(f"[REGISTER SUCCESS] User '{form.username.data}' registered successfully.")
            
            return redirect(url_for('auth.Login'))
        except Exception as e:
            db_session.rollback()
            current_app.logger.error(f"[REGISTER ERROR] Failed to register '{form.username.data}': {e}")
        finally:
            db_session.remove()  

    return render_template('Register.html', form=form)


# User Logout Route
@auth_bp.route('/logout', methods=['GET'])  
@login_required
def Logout():
    try:        
        logout_user()
        session.clear()

        current_app.logger.info("[LOGOUT] User logged out successfully.")
        return redirect(url_for('auth.Login'))
    except Exception as e:
        current_app.logger.error(f"[LOGOUT ERROR] Failed to logout: {e}")
        return redirect(url_for('auth.Login'))
