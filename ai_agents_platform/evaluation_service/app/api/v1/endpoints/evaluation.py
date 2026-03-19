from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
import json
from sqlalchemy.orm import Session
from app.schemas.schemas import EvaluationResponse
from app.core.database import get_db
from app.repositories.evaluation_repository import EvaluationRepository
from app.services.evaluation_service import EvaluationServiceHandler

router = APIRouter()

@router.post("/evaluation", response_model=EvaluationResponse)
async def evaluation_endpoint(
    action: str = Form(...),
    parameters: str = Form("{}"),
    audio: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        # If parameters is a JSON string, parse it
        try:
            params = json.loads(parameters)
        except:
            params = {}
            
        repository = EvaluationRepository(db)
        service = EvaluationServiceHandler(repository)
        
        result = await service.process_and_save(action, params, audio)
        return EvaluationResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


