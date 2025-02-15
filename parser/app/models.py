from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_login import UserMixin

Base = declarative_base()

# Define the User database model
class User(Base, UserMixin):  
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    logs = relationship('Log', back_populates='user', cascade='all, delete-orphan')

# Define the Log database model
class Log(Base):  
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False)
    timestamp = Column(String(50), nullable=False)
    method = Column(String(10), nullable=False)
    url = Column(String(100), nullable=False)
    protocol = Column(String(10), nullable=False)
    status = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    referrer = Column(String(100), nullable=False)
    user_agent = Column(String(100), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='logs')

# Create database engine and session
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
Session = SessionLocal()
