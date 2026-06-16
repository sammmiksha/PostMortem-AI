# PostMortem-AI

AI-powered Incident Intelligence Engine.

## Features

- Incident submission
- AI-generated incident reports
- PostgreSQL storage
- React frontend
- FastAPI backend
- Ollama local LLM integration

## Tech Stack

- React
- FastAPI
- PostgreSQL
- SQLAlchemy
- Ollama
- Qwen2.5:3B

## Run Backend

```bash
uvicorn main:app --reload
Run Frontend
npm run dev

---

### Create a Release Tag

Locally:

```bash
git tag -a v0.1.0 -m "Part 1 complete"
git push origin v0.1.0
