from pydantic import BaseModel
from typing import Dict, Any

class EvaluationRequest(BaseModel):
    action: str
    parameters: Dict[str, Any]

class EvaluationResponse(BaseModel):
    result: Dict[str, Any]
