from pydantic import BaseModel
from typing import List, Dict, Any

class QuestionRequest(BaseModel):
    topic: str
    difficulty: str
    num_questions: int = 5

class QuestionResponse(BaseModel):
    questions: List[str]

class AgentRequest(BaseModel):
    action: str
    topic: str = "General English"
    difficulty: str = "Medium"
    count: int = 5
    length_words: int = 150
    parameters: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    result: Dict[str, Any]
