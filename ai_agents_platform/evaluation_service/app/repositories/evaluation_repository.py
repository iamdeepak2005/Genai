from sqlalchemy.orm import Session
from app.models.domain import EvaluationResult

class EvaluationRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_evaluation(self, action: str, reference_audio: str, text_content: str, result_json: dict) -> EvaluationResult:
        db_record = EvaluationResult(
            action=action,
            reference_audio=reference_audio,
            text_content=text_content,
            result_json=result_json
        )
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record
