from flask import Blueprint, render_template, redirect, url_for,current_app, session
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required
from app.Forms.forms import upload_form
import re , json, os, ipaddress

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

            filter =form.sortby.data
            current_app.logger.info(f"sort used {filter} by user {session['username']}")
            sorted_data = sorting(json_file_path, filter )
            if sorted_data:
                current_app.logger.info(f"Log file {filename} sorted successfully by user {session['username']}")
                return redirect(url_for("api.Login"))
        else:
            return redirect(url_for("service.Upload_Parse"))

    return render_template('Homee.html', form=form)

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
                filtered_data = {field: log_data[field] for field in selected_fields if field in log_data}
                log_list.append(filtered_data)

        # Create a separate directory for storing JSON files
        json_dir = os.path.join("app", "json_logs")
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        json_file_path = os.path.join(json_dir, "log.json")  # Save JSON in separate directory
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(log_list, json_file, indent=4)
            
        return json_file_path  # Return JSON data as a string
       
    except Exception as e:
        current_app.logger.error(f"Error parsing log file: {e}")
        return None
 
def sorting(json_file_path, filter):
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not data:
            current_app.logger.warning("Sorting failed: No data in JSON file.")
            return None
        
        if filter == "ip":
            # Convert IP address strings to actual IP objects for proper sorting
            sorted_data = sorted(data, key=lambda x: ipaddress.ip_address(x.get(filter, '0.0.0.0')))
        else:
            # Sort normally for other fields
            sorted_data = sorted(data, key=lambda x: x.get(filter, ''))

        # Save sorted data back to the same file
        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(sorted_data, file, indent=4)

        return json_file_path  # Return the updated file path

    except Exception as e:
        current_app.logger.error(f"Error sorting log file: {e}")
        return None  # Return None if sorting fails
    