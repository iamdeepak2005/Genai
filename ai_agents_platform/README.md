# AI Agents Platform

A high-performance microservices-based AI Agents Platform for educational content generation and automated evaluation. Built with **FastAPI**, **LangChain**, **OpenAI**, **FFmpeg**, and **Whisper**.

## Project Architecture

The platform consists of two specialized microservices:

1.  **Admin Service**: Handles AI-driven content generation like grammar questions and reading passages.
2.  **Evaluation Service**: Handles speech-to-text processing, pronunciation grading, and text analysis.

---

## 🛠️ Services Overview

### 1. Admin Service (Port 8000)
Orchestrates educational content generation logic.
- **Endpoint**: `POST /api/v1/admin/qb`
- **Actions**:
    - `generate_questions`: Create multiple-choice questions based on topic, difficulty, and count.
    - `generate_passage`: Create a reading passage along with assessment questions.
- **Payload Parameters**:
    - `topic`: (String) e.g., "Space Exploration"
    - `difficulty`: (String) "Easy", "Medium", "Hard"
    - `count`: (Integer) Number of questions to generate.
    - `length_words`: (Integer) Length of the passage (for `generate_passage`).

### 2. Evaluation Service (Port 8001)
Handles audio processing and multilingual evaluation.
- **Endpoint**: `POST /api/v1/evaluation` (using `multipart/form-data`)
- **Key Features**:
    - **Audio Processing**: Uses **FFmpeg** via `pydub` for audio normalization.
    - **Speech-to-Text**: Integrated with local **OpenAI Whisper** for high-accuracy transcription.
    - **Tone & Pronunciation**: Evaluates user speech against expected text.
- **Actions**:
    - `evaluate_all`: Runs grammar, vocabulary, pronunciation, and reading speed evaluations.
    - `pronunciation_eval`: Specifically checks for mispronounced words.
    - `reading_eval`: Calculates Words Per Minute (WPM) and accuracy.
    - `grammar_eval`: Checks grammatical correctness of spoken/written input.

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key (Set in `.env`)
- FFmpeg (Installed automatically in Docker)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/iamdeepak2005/Genai.git
   cd Genai/ai_agents_platform
   ```

2. Configure environment variables in `.env`:
   ```env
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=postgresql://user:pass@db:5432/evaldb
   ```

3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

---

## 📖 API Usage Examples

### Admin Service: Generate Questions
```bash
curl -X POST http://localhost:8000/api/v1/admin/qb \
-H "Content-Type: application/json" \
-d '{
  "action": "generate_questions",
  "parameters": {
    "topic": "Python Programming",
    "difficulty": "Medium",
    "count": 5
  }
}'
```

### Evaluation Service: Audio Evaluation
To evaluate an audio file, use a multi-part form request:
```bash
curl -X POST http://localhost:8001/api/v1/evaluation \
-F "action=evaluate_all" \
-F 'parameters={"expected_text": "The solar system consists of eight planets.", "reading_time_seconds": 10}' \
-F "audio=@recording.wav"
```

---

## 📁 Repository Structure
```text
.
├── admin_service/          # Content generation microservice
├── evaluation_service/     # Speech & text evaluation microservice
│   ├── app/
│   │   ├── agents/         # Evaluation Agent with Whisper integration
│   │   ├── services/       # Audio handling logic
│   │   └── uploads/        # Temporary audio storage
├── docker-compose.yml      # Orchestration for all services
└── .gitignore              # Clean repository management
```

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.
