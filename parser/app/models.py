from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_login import UserMixin   

engine = create_engine('sqlite:///parser.db', echo=True)
Base = declarative_base()

# Define the User database model
class User(Base, UserMixin):  
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

@property
def is_active(self):
    return True

@property
def is_anonymous(self):
    return False

@property
def is_authenticated(self):
    return True

# Create database engine and session

SessionLocal = sessionmaker(bind=engine)
Session = SessionLocal()

Base.metadata.create_all(engine)
