from flask import Blueprint, render_template, redirect, url_for, session, current_app, jsonify
from app.forms import URLForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required
from sqlalchemy.orm import scoped_session
from function.functions import fetch_store_file, save_parse_logs_json


# Blueprint for authentication
service_bp = Blueprint('auth', __name__)  

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address, default_limits=["5 per minute"])

@service_bp.route('/fetch', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
@login_required
def fetch_save():
    form = URLForm()

    if form.validate_on_submit():
        try:
            fetch_store_file(form.url.data)
            current_app.logger.info(f"[URL PARSED] URL '{form.url.data}' parsed successfully.")
            return redirect(url_for('service_bp.parse_save'))
        except Exception as e:
            current_app.logger.error(f"[URL PARSE ERROR] Unexpected error for '{form.url.data}': {e}")
    return render_template('fetch.html', form=form)

@service_bp.route('/parse', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
@login_required
def parse_save():
    try:
        save_parse_logs_json()
        current_app.logger.info("[LOG PARSED] Log file parsed successfully.")
        return redirect(url_for('service_bp.display'))
    except Exception as e:
        current_app.logger.error(f"[LOG PARSE ERROR] Unexpected error: {e}")