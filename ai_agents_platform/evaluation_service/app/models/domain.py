from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from app.core.database import Base

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    reference_audio = Column(String, nullable=True)
    text_content = Column(String, nullable=True)
    result_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
