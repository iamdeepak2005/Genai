from app.agents.admin_agent import AdminAgent
from app.repositories.generation_repository import GenerationRepository

class GenerationService:
    def __init__(self, repository: GenerationRepository):
        self.agent = AdminAgent()
        self.repository = repository

    def process_and_save(self, action: str, topic: str, difficulty: str, count: int, length_words: int, parameters: dict) -> dict:
        # Merge top-level fields into parameters for the agent
        processed_params = parameters.copy()
        if "topic" not in processed_params: processed_params["topic"] = topic
        if "difficulty" not in processed_params: processed_params["difficulty"] = difficulty
        if "count" not in processed_params: processed_params["count"] = count
        if "length_words" not in processed_params: processed_params["length_words"] = length_words

        print(f"--- Calling agent with params: {processed_params} ---")
        result = self.agent.process_request(action, processed_params)
        
        print(f"--- Saving results to repository for action: {action} ---")
        self.repository.save_generation(
            action=action, 
            topic=processed_params.get("topic"), 
            difficulty=processed_params.get("difficulty"), 
            result_json=result
        )
        return result
