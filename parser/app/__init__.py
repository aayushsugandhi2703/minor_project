from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
from flask_login import LoginManager
from app.Models.models import User, Session
import os
from prometheus_client import Counter

jwt = JWTManager()
def create_app():
    app = Flask(__name__)
    
# configurations
    from config import Config 
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"] = "app/uploads"

# initialize the json web token
    jwt.init_app(app)

# initialize the Prometheus Directory
    prometheus_dir = app.config.get('PROMETHEUS_MULTIPROC_DIR', './prometheus_data')

    # If the directory doesn't exist, create it
    if not os.path.exists(prometheus_dir):
        os.makedirs(prometheus_dir)

    # Simple: remove all files inside the directory
    for file in os.listdir(prometheus_dir):
        file_path = os.path.join(prometheus_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Set the environment variable
    os.environ['PROMETHEUS_MULTIPROC_DIR'] = prometheus_dir

#initializing the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'api.Login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Session.query(User).get(int(user_id))
    
#initializing hte limiter
    limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
    limiter.init_app(app)
    
#configurint the logger
    def setup_logger(logger):
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(message)s'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')

    setup_logger(app.logger)

#import the blueprints
    from app.api.routes import api_bp
    from app.service.routes import service_bp
    from app.matrix.routes import matrix_bp

    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(service_bp, url_prefix='/service')
    app.register_blueprint(matrix_bp, url_prefix='/matrix')

    
    return app