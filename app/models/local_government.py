from enum import unique
from operator import index
from sqlalchemy import Column, Integer, String
from app.database.session import Base




class LocalGovernment(Base):
    __tablename__ = 'local_government'
    id = Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    code =Column(String, nullable=False, unique=True, index=True)