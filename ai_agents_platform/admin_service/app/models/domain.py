from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from app.core.database import Base

class ContentGeneration(Base):
    __tablename__ = "content_generations"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    theme_topic = Column(String)
    difficulty = Column(String, nullable=True)
    passage = Column(String, nullable=True)
    question = Column(String, nullable=True)
    options = Column(JSON, nullable=True)
    explanation = Column(String, nullable=True)
    correct_answer = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
