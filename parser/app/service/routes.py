from flask import Blueprint, render_template, request, current_app, Response
from flask_login import login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.functions import reuse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, Counter

service_bp = Blueprint('servie', __name__)

# initializing the limiter with default limits
limiter = Limiter(key_func=get_remote_address, default_limits=["10 per minute"])

# Create a counter metric
count_request = Counter('total_requests', 'Total HTTP Requests', ['method', 'endpoint'])

@login_required
@limiter.limit("10 per minute")
@service_bp.route('/upload', methods=['GET', 'POST'])
def upload_select():
#Upload logs and allow field selection.
    count_request.labels(method = request.method, endpoint='/upload').inc()
    if request.method == 'POST':
        link = request.form.get('link')  # Get link from form
        reuse.fetch(link)  # Fetch logs from the link
        parsed_logs = reuse.parse_logs()  # Parse logs

# Get selected fields from form (checkbox values)
        selected_fields = request.form.getlist('fields')
        if not selected_fields:
            return ({"error": "No fields selected!"}), 400
        
# Filter logs based on selected fields
        filtered_logs = [
            {field: log[field] for field in selected_fields if field in log}
            for log in parsed_logs
        ]

        current_app.logger.info(f"Logs uploaded and parsed. Fields selected: {selected_fields}")
        return render_template("logs.html", logs=filtered_logs, fields=selected_fields)

    return render_template("select_fields.html")  # Show field selection form


@login_required
@limiter.limit("5 per minute")
def sort_logs():
#Sort logs based on selected field and display chosen fields
    count_request.labels(method=request.method, endpoint='/sort').inc()
    if request.method == 'POST':
        parsed_logs = reuse.parse_logs()  

# Get selected fields and sorting criteria from the form
        selected_fields = request.form.getlist('fields')
        sort_field = request.form.get('sort_field')

        if not selected_fields or not sort_field:
            return ({"error": "Please select at least one field and a sort field!"}), 400

# Sort logs in ascending order based on the selected sort field
        try:
            sorted_logs = sorted(parsed_logs, key=lambda x: x.get(sort_field, ''))
        except KeyError:
            return ({"error": f"Invalid sort field: {sort_field}"}), 400
        
        current_app.logger.info(f"Logs sorted by {sort_field}. Fields selected: {selected_fields}")
        
        return render_template("sorted_logs.html", logs=sorted_logs, fields=selected_fields)

    return render_template("sort_select.html")

@service_bp.route('/metrics')
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)