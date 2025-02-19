from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
from flask_login import LoginManager
import os

def create_app():
    app = Flask(__name__)

# Setting the logger
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

# setting the limiter
    limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
    limiter.init_app(app)

#setting up login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

# setting the config file
    from config import Config
    app.config.from_object(Config)

#Setting up Blueprints
    from app.auth.routes import auth_bp
    from app.service.routes import service_bp
    app.register_blueprint(auth_bp, url_prefix='/register')
    app.register_blueprint(service_bp, url_prefix='/upload')
    return app