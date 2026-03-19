from fastapi import FastAPI
from app.api.v1.endpoints import evaluation
from app.core.database import engine
from app.models import domain

# Create database tables
domain.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Evaluation Service API",
    description="Microservice for handling Evaluation Agent tasks",
    version="1.0.0"
)

app.include_router(evaluation.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
