from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from backend.database import Base

class RiskMetric(Base):
    __tablename__ = "risk_metrics"

    id = Column(Integer, primary_key=True, index=True)
    crowd_count = Column(Integer)
    avg_density = Column(Float)
    max_density = Column(Integer)
    risk_score = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    risk_score = Column(Float)
    status = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
