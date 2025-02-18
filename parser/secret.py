import os

def get_secret_key():
    return os.getenv('SECRET_KEY', 'a_default_secret_key')