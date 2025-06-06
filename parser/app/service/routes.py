from flask import Blueprint, render_template, redirect, url_for,current_app, session, jsonify, request
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required
from app.Forms.forms import upload_form
import re , json, os, ipaddress
from email.message import EmailMessage
import smtplib, ssl, threading
from prometheus_client import Histogram
from app.service.log_classifier import LogClassifier

service_bp = Blueprint('service', __name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

classifier = LogClassifier()

# Histogram to track the latency of the login request
Request_latency_upload = Histogram('upload_latency', 'Histogram tracking upload latency', buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10])
Request_latency_output = Histogram('output_latency', 'Histogram tracking output latency', buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10])


@service_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@limiter.limit("5 per minute")
def Upload_Parse():
    with Request_latency_upload.time(): 

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
            classifier.train_model(file_path)  # After parsing the uploaded file

            # Get the selected fields from the form
            selected_fields = form.fields.data  # List of selected field names
            session['selected_fields'] = selected_fields

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
                    return redirect(url_for("service.Output"))
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
    
@service_bp.route('/output', methods=['GET', 'POST'])
@login_required
def Output():
    with Request_latency_upload.time():

        json_dir = os.path.join("app", "json_logs")
        json_file_path = os.path.join(json_dir, "log.json")

        if not os.path.exists(json_file_path):
            return "No data available"
        
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        selected_entry = data[:15]
        selected_fields = session.get('selected_fields', [])

        receiver_email = session['email']  # Grabbing email from session
        app = current_app._get_current_object()

        # Passing email and file path to the thread
        argss = (receiver_email, json_file_path)
        email_thread = threading.Thread(
            target=send_email,
            args=(app,receiver_email, json_file_path)
        )
        email_thread.start()

        return render_template(
            'output.html',
            logs=selected_entry,  # Show the first 15 entries
            email=receiver_email,  # Show the email address to user
            fields=selected_fields  # Show the selected fields to user
        )

def send_email(app, receiver_email, json_file_path):
    with app.app_context():  # Now app context is valid!
        try:
            sender_email = "aayush.sugandhi@gmail.com"
            # password = os.getenv('APP_PASSWORD_GMAIL')

            subject = "Log File"
            body = """
                This is an automated email from the server.
                Please find the attached log file.
                """

            em = EmailMessage()
            em['from'] = sender_email
            em['to'] = receiver_email
            em['subject'] = subject
            em.set_content(body)

            #  Attach the JSON log file
            with open(json_file_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(json_file_path)
                em.add_attachment(file_data, maintype='application', subtype='json', filename=file_name)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(sender_email, password)
                server.send_message(em)

            current_app.logger.info(f"Log file sent to {receiver_email} by Owner")

        except FileNotFoundError:
            current_app.logger.error(f"File {json_file_path} not found")

        except Exception as e:
            current_app.logger.error(f"Failed to send log file: {str(e)}")

UPLOAD_FOLDER = "uploads"  # make sure this exists

@service_bp.route('/dos_ui')
@login_required
def dos_ui():
    return render_template("detect.html")

@service_bp.route('/uploading', methods=['GET', 'POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    session['uploaded_file'] = file_path
    return redirect(url_for("service.detect_dos"))

@service_bp.route('/detect_dos', methods=['GET', 'POST'])
@login_required
def detect_dos():
    file_path = session.get("uploaded_file")

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "No uploaded file found"}), 400

    classifier = LogClassifier(request_threshold=100, interval_threshold=2, error_threshold=20)
    classifier.train_model(file_path)
    suspected_ips = classifier.predict_suspected_ips()
    features = classifier.get_ip_features()

    current_app.logger.info(f"Suspected DoS IPs: {suspected_ips}")

    return jsonify({
        "suspected_ips": suspected_ips,
        "ip_features": features
    })