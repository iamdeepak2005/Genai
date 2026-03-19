from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import AgentRequest, AgentResponse
from app.core.database import get_db
from app.repositories.generation_repository import GenerationRepository
from app.services.generation_service import GenerationService

router = APIRouter()

@router.post("/qb", response_model=AgentResponse)
async def admin_qb_endpoint(request: AgentRequest, db: Session = Depends(get_db)):
    try:
        repository = GenerationRepository(db)
        service = GenerationService(repository)
        
        result = service.process_and_save(
            action=request.action,
            topic=request.topic,
            difficulty=request.difficulty,
            count=request.count,
            length_words=request.length_words,
            parameters=request.parameters
        )
        return AgentResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


