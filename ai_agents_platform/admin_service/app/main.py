from fastapi import FastAPI
from app.api.v1.endpoints import qb
from app.core.database import engine
from app.models import domain

# Create database tables
domain.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Admin Service API",
    description="Microservice for handling Admin Agent tasks",
    version="1.0.0"
)

app.include_router(qb.router, prefix="/api/v1/admin")

@app.get("/health")
def health_check():
    return {"status": "ok"}
