import os
import shutil
from fastapi import UploadFile
from app.agents.evaluation_agent import EvaluationAgent
from app.repositories.evaluation_repository import EvaluationRepository

class EvaluationServiceHandler:
    def __init__(self, repository: EvaluationRepository):
        self.agent = EvaluationAgent()
        self.repository = repository
        # Ensure uploads directory exists
        os.makedirs("uploads", exist_ok=True)

    async def process_and_save(self, action: str, parameters: dict, audio_file: UploadFile = None) -> dict:
        audio_path = None
        if audio_file:
            audio_path = f"uploads/{audio_file.filename}"
            with open(audio_path, "wb") as buffer:
                shutil.copyfileobj(audio_file.file, buffer)
            parameters["user_audio_ref"] = audio_path

        result = await self.agent.process_request(action, parameters)
        
        reference_audio = parameters.get("user_audio_ref", "none")
        text_content = parameters.get("text", "")
        
        self.repository.save_evaluation(
            action=action,
            reference_audio=reference_audio,
            text_content=text_content,
            result_json=result
        )
        return result
