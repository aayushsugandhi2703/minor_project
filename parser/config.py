from secret import get_secret_key

class Config:

#for secret key
    SECRET_KEY = get_secret_key()

#for database
    SQLALCHEMY_DATABASE_URI= 'sqlite:///databse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

#for JWT and cookies
    JWT_SECRET_KEY = get_secret_key()
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = True
    JWT_ACCESS_TOKEN_EXPIRES = 100
    JWT_REFRESH_TOKEN_EXPIRES = 100

# for redis cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = '0'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 3600
