from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Engine = create_engine('''sqlite:///database.db''')

Base = declarative_base()

class User(UserMixin,Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    phone = Column(Integer, nullable = False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

@property
def is_active(self):
    return True

@property
def is_anonymous(self):
    return False

@property
def is_authenticated(self):
    return True

session = sessionmaker(bind=Engine)

Session = session()

Base.metadata.create_all(Engine)