# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataHistory(Base):
    __tablename__ = "data_history1"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    name = Column(String(255))
    reading_string = Column(String(1024))
