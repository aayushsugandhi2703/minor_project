from flask import Blueprint, render_template, redirect, url_for, flash,current_app, session
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required
from app.Forms.forms import upload_form
import re, requests , json, os

service_bp = Blueprint('service', __name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@login_required
@limiter.limit("5 per minute")
@service_bp.route('/upload', methods=['GET', 'POST'])
def Upload_Parse():
    form = upload_form()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        upload_folder = current_app.config.get("UPLOAD_FOLDER", "app/uploads")

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)  # Create folder if not exists

        file_path = os.path.join(upload_folder, filename)

        with open(file_path, "wb") as f:
            f.write(file.read())  # Save the file manually

        session["uploaded_file"] = file_path #added to session so that it can be accessed in the next route
        current_app.logger.info(f"File {filename} uploaded successfully by user {session['username']}")

# Now parsing the log file
        parsed_logs = parse_log_file(file_path)

        if parsed_logs:
            print(parsed_logs)
            '''return redirect(url_for("service.parse_file"))  # Redirect to parsing page'''

    return render_template('Home.html', form=form)

def parse_log_file(file_path):
    log_list = []

    # Regular expression pattern for parsing logs
    pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) '
        r'(?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+) '
        r'"(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    )

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            logs = file.readlines()  # Read log lines

        for log in logs:
            match = pattern.search(log)
            if match:
                log_list.append(match.groupdict())  # Convert match to dictionary

        return log_list
    except Exception as e:
        current_app.logger.error(f"Error parsing log file: {e}")
        return []