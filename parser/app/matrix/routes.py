from flask import Blueprint, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, multiprocess

matrix_bp = Blueprint('matrix', __name__)

@matrix_bp.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    
    # Collect multiprocess metrics
    multiprocess.MultiProcessCollector(registry)
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)
