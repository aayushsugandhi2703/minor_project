from flask import Blueprint, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, multiprocess

matrix_bp = Blueprint('matrix', __name__)

@matrix_bp.route('/metrics')
def metrics():
    
    # for using it with gunicorn 
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)

    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)
    '''
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    '''