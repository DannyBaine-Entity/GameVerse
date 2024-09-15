from sqlalchemy import Column, Integer, String, Text
from .database import db



class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(60), unique=True, nullable=False)
    password = Column(String(60), nullable=False)