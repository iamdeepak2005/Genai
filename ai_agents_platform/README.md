# AI Agents Platform

This project sets up a microservices-based AI Agents Platform using FastAPI and Docker.

## Services Architecture

The application is split into two independent microservices:
1. **Admin Service (`/api/v1/admin/qb`)**
2. **Evaluation Service (`/api/v1/evaluation`)**

Both microservices follow a clean modular structure (layered architecture pattern):
- `app/api/v1/endpoints`: Contains FastAPI routers.
- `app/agents`: Combines multiple tools and orchestrates logic for an integrated workflow.
- `app/tools`: The atomic AI tools that handle grammar, passages, pronunciations, validations, etc.
- `app/models/schemas.py`: Pydantic models for request/response serialization.

### 1. Admin Agent (admin_service)
Orchestrates educational generation logic.
- **Port**: 8000
- **Endpoint**: `POST /api/v1/admin/qb`
- **Tools Included**:
  - `Grammar Question Generator Tool`: Generates grammar-based questions.
  - `Passage Generator Tool`: Generates passages for evaluation.

### 2. Evaluation Agent (evaluation_service)
Orchestrates grading, evaluating, and parsing logic.
- **Port**: 8001
- **Endpoint**: `POST /api/v1/evaluation`
- **Tools Included**:
  - `Grammar Evaluation Tool`: Evaluates grammar for a given passage.
  - `Pronunciation Evaluation Tool`: Evaluates pronunciation based on user performance.
  - `Reading Evaluation Tool`: Classifies users as "Good Reader," "Average Reader," or "Bad Reader."
  - `Vocabulary Richness Analyzer Tool`: Assesses vocabulary diversity in a text.
  - `Structure Validator Tool`: Validates sentence & paragraph structure.

## Running the Platform

Ensure you have Docker and Docker Compose installed on your machine.

1. Navigate to the root directory `ai_agents_platform`.
2. Run the platform via Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The services will be fully interactive via Swagger UI:
   - Admin Service Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Evaluation Service Documentation: [http://localhost:8001/docs](http://localhost:8001/docs)

## Sample Payload

**Admin Service (Generate Questions):**
```bash
curl -X POST http://localhost:8000/api/v1/admin/qb \
-H "Content-Type: application/json" \
-d '{
  "action": "generate_questions",
  "parameters": {
    "topic": "English Nouns",
    "difficulty": "Easy",
    "count": 3
  }
}'
```

**Evaluation Service (Evaluate All):**
```bash
curl -X POST http://localhost:8001/api/v1/evaluation \
-H "Content-Type: application/json" \
-d '{
  "action": "evaluate_all",
  "parameters": {
    "text": "This is a quick reading passage.",
    "user_audio_ref": "audio001.mp3",
    "expected_text": "This is a quick reading passage."
  }
}'
```
