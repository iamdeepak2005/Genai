from sqlalchemy.orm import Session
from app.models.domain import ContentGeneration

class GenerationRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_generation(self, action: str, topic: str, difficulty: str, result_json: dict) -> list:
        records = []
        q_list = result_json.get("questions", [])
        opt_list = result_json.get("options", [])
        exp_list = result_json.get("explanations", [])
        ans_list = result_json.get("correct_answers", [])
        passage = result_json.get("passage")
        
        # Ensure we have matching counts if one list is shorter (shouldn't happen with correct agent logic)
        num_questions = len(q_list)
        
        for i in range(num_questions):
            db_record = ContentGeneration(
                action=action,
                theme_topic=topic,
                difficulty=difficulty,
                passage=passage,
                question=q_list[i],
                options=opt_list[i] if i < len(opt_list) else {},
                explanation=exp_list[i] if i < len(exp_list) else "",
                correct_answer=ans_list[i] if i < len(ans_list) else ""
            )
            self.db.add(db_record)
            records.append(db_record)
            
        self.db.commit()
        for r in records:
            self.db.refresh(r)
        return records
