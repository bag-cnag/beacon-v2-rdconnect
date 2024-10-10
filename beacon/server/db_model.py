from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    entity_id = Column(String(300), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    username = Column(String(120), nullable=False)
    groups = Column(String(300), nullable=False)
    endpoint = Column(String(1000), nullable=False)
    method = Column(String(120), nullable=False)
    content = Column(JSONB)