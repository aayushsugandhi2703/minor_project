from flask import Blueprint, render_template, redirect, url_for, flash,current_app, session
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required
from app.Forms.forms import upload_form
import re, requests , json, os

service_bp = Blueprint('service', __name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@service_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@limiter.limit("5 per minute")
def Upload_Parse():
    form = upload_form()
    
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "app/uploads")

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, filename)

        with open(file_path, "wb") as f:
            f.write(file.read())

        session["uploaded_file"] = file_path  # Save file path in session

        # Get the selected fields from the form
        selected_fields = form.fields.data  # List of selected field names

        current_app.logger.info(f"File {filename} uploaded successfully by user {session['username']}")

        # Parse log file and filter fields
        json_file_path = parse_log_file(file_path, selected_fields)

        if json_file_path:
            current_app.logger.info(f"Log file {filename} parsed successfully by user {session['username']}")
            return redirect(url_for("service.sorting_op"))
        else:
            return redirect(url_for("service.Upload_Parse"))

    return render_template('Home.html', form=form)

def parse_log_file(file_path, selected_fields):
    log_list = []
    pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) '
        r'(?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+) '
        r'"(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    )

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            logs = file.readlines()

        for log in logs:
            match = pattern.search(log)
            if match:
                log_data = match.groupdict()  # Convert log entry to dictionary
                
                # Filter log data based on user selection
                filtered_data = {field: log_data[field] for field in selected_fields}
                log_list.append(filtered_data)

        json_data = json.dumps(log_list, indent=4)  # Convert to JSON

        # Create a separate directory for storing JSON files
        json_dir = os.path.join("app", "json_logs")
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        json_file_name = os.path.basename(file_path).replace(".log", ".json")
        json_file_path = os.path.join(json_dir, json_file_name)  # Save JSON in separate directory
        
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json_file.write(json_data)

        return json_file_path  # Return JSON data as a string

    except Exception as e:
        current_app.logger.error(f"Error parsing log file: {e}")
        return []

'''    
@login_required
@limiter.limit("5 per minute")
@service_bp.route('/output', methods=['GET', 'POST'])
def sorting_op():
'''