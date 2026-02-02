from app.database import Base
from sqlalchemy import String, Integer, Column, DateTime
from datetime import datetime



class Querie(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    cluster = Column(Integer, primary_key=True, index=True)
    latency_ms = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)


 