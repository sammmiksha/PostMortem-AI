<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=2d1f5e,7c5cbf,b39ddb&height=140&section=header&text=PostMortem%20AI&fontSize=40&fontColor=ffffff&fontAlignY=55&desc=AI-powered%20Incident%20Intelligence%20Engine&descAlignY=78&descSize=14" />

![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-2d1f5e?style=flat-square&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-b39ddb?style=flat-square)
![Version](https://img.shields.io/badge/version-v0.1.0-7c5cbf?style=flat-square)

*Transforms raw incident reports into structured postmortem analyses — locally, privately, intelligently.*

</div>

---

## overview

PostMortem AI helps engineering teams document, analyze, and learn from incidents by automatically generating structured incident reports and postmortem summaries.

The platform combines a **React frontend**, **FastAPI backend**, **PostgreSQL database**, and **locally hosted LLMs via Ollama** to provide an end-to-end incident intelligence workflow — with no data leaving your infrastructure.

---

## current status

| Phase | Status |
|---|---|
| Phase 1 — Core Incident Intelligence Platform | ✅ Complete |
| Phase 2 — Root Cause Intelligence | 🚧 In Progress |
| Phase 3 — Enterprise Intelligence | 🔮 Planned |

---

## features

### ✅ phase 1 — core platform `v0.1.0`

- Incident submission and management
- AI-generated incident reports via local LLM
- PostgreSQL persistence layer
- FastAPI REST API with structured endpoints
- React-based user interface
- Ollama integration for on-device LLM inference (Qwen2.5:3B)
- Structured incident storage and retrieval

### 🚧 phase 2 — root cause intelligence

- Automated root cause extraction
- Incident severity classification
- Timeline reconstruction
- Action item generation
- Executive summary generation
- Multi-incident trend analysis

### 🔮 phase 3 — enterprise intelligence

- Incident knowledge base
- Semantic search across incidents
- Retrieval-Augmented Generation (RAG)
- Team dashboards and analytics
- Incident similarity detection
- Predictive incident insights

---

## tech stack

| layer | technology |
|---|---|
| **Frontend** | React |
| **Backend** | FastAPI · SQLAlchemy |
| **Database** | PostgreSQL |
| **AI / LLM** | Ollama · Qwen2.5:3B |
| **Language** | Python · JavaScript |

---

## getting started

### prerequisites

- Python 3.10+
- Node.js v18+
- PostgreSQL running locally
- [Ollama](https://ollama.com/) installed with `qwen2.5:3b` pulled

```bash
ollama pull qwen2.5:3b
```

### run the backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload
```

> API available at `http://localhost:8000`

### run the frontend

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

> App available at `http://localhost:5173`

---

## release

### v0.1.0 — Phase 1 Complete

Phase 1 completion release. Core incident intelligence platform is fully functional with local LLM-powered report generation.

```bash
git tag -a v0.1.0 -m "Phase 1 Complete"
git push origin v0.1.0
```

---

## license

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=2d1f5e,7c5cbf,b39ddb&height=100&section=footer" />

*Built by [Samiksha Patil](https://github.com/sammmiksha) — Mumbai, India*

</div>
