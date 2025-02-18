from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db', echo=True)

Base = declarative_base()

class User(UserMixin, Base):
    
    __tablename__ = 'users_data'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
Session = sessionmaker( bind = engine )

session_db = Session()

Base.metadata.create_all(engine)

