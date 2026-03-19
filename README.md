# GenAI Project

Automating educational content and evaluation using advanced AI agents.

## Project Structure

This repository contains the **AI Agents Platform**, a microservices-based system featuring:

*   **[Admin Service](./ai_agents_platform/admin_service)**: Educational content generation (grammar, passages).
*   **[Evaluation Service](./ai_agents_platform/evaluation_service)**: Audio transcription (Whisper), FFmpeg processing, and student performance evaluation.

Check the **[Platform README](./ai_agents_platform/README.md)** for detailed instructions on running and using the services.

## Quick Start (with Docker)

```bash
cd ai_agents_platform
docker-compose up --build
```
