<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=2d1f5e,7c5cbf,b39ddb&height=140&section=header&text=PostMortem%20AI&fontSize=40&fontColor=ffffff&fontAlignY=55&desc=AI-powered%20Incident%20Intelligence%20Engine&descAlignY=78&descSize=14" />

![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-2d1f5e?style=flat-square&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-b39ddb?style=flat-square)
![Version](https://img.shields.io/badge/version-v5.0.0-7c5cbf?style=flat-square)

*Transforms raw incident reports into structured postmortem analyses, Git root cause tracing, RAG memory retrieval, and preventative action — locally, privately, intelligently.*

</div>

---

## overview

PostMortem AI helps engineering teams document, analyze, correlate, and learn from incidents by automatically generating structured postmortems, isolating root cause commits in Git history, searching historical incident memory using RAG vectors, auto-generating Pytest regression tests and Prometheus alert rules, and tracking enterprise reliability analytics.

The platform combines a **React frontend**, **FastAPI backend**, **PostgreSQL database with pgvector**, and **locally hosted LLMs via Ollama** to provide an end-to-end incident intelligence workflow — with no data leaving your infrastructure.

---

## current status

| Phase | Status |
|---|---|
| Phase 1 — Core Incident Intelligence Platform | Complete |
| Phase 2 — Git Root Cause Analyzer | Complete |
| Phase 3 — Incident Memory System (RAG + Knowledge Base) | Complete |
| Phase 4 — Prevention Intelligence Engine | Complete |
| Phase 5 — Production Platform & Enterprise Analytics | Complete |

---

## features

### Phase 1 — Core Platform `v0.1.0`

- Incident submission and management
- AI-generated incident reports via local LLM
- PostgreSQL persistence layer
- FastAPI REST API with structured endpoints
- React-based user interface
- Ollama integration for on-device LLM inference (Qwen2.5:3B)
- Structured incident storage and retrieval

### Phase 2 — Git Root Cause Analyzer `v2.0.0`

- Crash stack trace parser (extracting file, line number, function, error type)
- Multi-factor commit candidate ranking (File match +40, Function match +30, Recentness +20, Keyword similarity +20)
- AI commit reviewer analyzing diff patches and stack traces to assign confidence risk scores (e.g. 84% Risk)
- Git history scanner and patch diff inspector interface

### Phase 3 — Incident Memory System (RAG + Knowledge Base) `v3.0.0`

- 384d vector embedding system (`all-MiniLM-L6-v2`) for incident summaries and resolutions
- Hybrid RAG semantic similarity search (70% Vector Similarity + 15% Service match + 15% Error Type match)
- Automated pattern detection engine across 8 operational domains (`Database`, `Auth`, `Networking`, `Config`, `Caching`, `API`, `Infra`, `Security`)
- Knowledge base memory stats and failure category distribution charts

### Phase 4 — Prevention Intelligence Engine `v4.0.0`

- Pytest regression test auto-generator targeting root causes
- Prometheus & Grafana monitoring alert rule generator (`expr`, `for: 2m`, `severity: critical`)
- SRE operational runbook generator (`Symptoms`, `Diagnosis`, `Resolution`, `Escalation`)
- Architecture recommendation engine with risk reduction priority scoring (Critical/High/Medium/Low)
- Quality validation layer for generated test assertions, alert metrics, and runbook headers
- One-click prevention package JSON download (`prevention_package_database.json`)

### Phase 5 — Production Platform & Enterprise Analytics `v5.0.0`

- Multi-user authentication & JWT authorization with RBAC roles (`Admin`, `Engineer`, `Manager`, `Viewer`)
- Enterprise Integrations Hub: Auto-generates REST Jira issue payloads and Slack Block Kit incident alert broadcasts
- Reliability Analytics Engine: MTTR (Mean Time To Resolution), MTBF, System Availability SLA %, Repeat Incident Rate, and Technical Debt Index
- Production Docker containerization (`Dockerfile` and `docker-compose.yml`)

---

## tech stack

| layer | technology |
|---|---|
| **Frontend** | React · Vite · Modern CSS Design System |
| **Backend** | FastAPI · SQLAlchemy · PyJWT · Pydantic |
| **Database** | PostgreSQL · pgvector · SQLite Fallback |
| **AI / LLM / Vector** | Ollama (Qwen2.5:3B) · Sentence-Transformers (384d Embeddings) |
| **Version Control & Parsing** | GitPython · Python Regex StackTrace Parser |
| **Integrations & Monitoring** | Jira REST API · Slack Block Kit · Prometheus Alert Rules |
| **DevOps / Testing** | Docker · Docker Compose · Pytest |

---

## getting started

### prerequisites

- Python 3.10+
- Node.js v18+
- [Ollama](https://ollama.com/) installed with `qwen2.5:3b` pulled

```bash
ollama pull qwen2.5:3b
```

### run the backend

```bash
# Activate virtual environment
source backend/venv/bin/activate   # Linux/macOS
# or: .\backend\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn backend.main:app --reload --port 8000
```

> API available at `http://localhost:8000` | Swagger Docs at `http://localhost:8000/docs`

### run the frontend

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

> App available at `http://localhost:5173`

### run with Docker Compose

```bash
docker-compose up --build
```

---

## release

### v5.0.0 — Complete Platform Release (Phases 1–5 Complete)

All 5 phases of the Master Vision Roadmap are fully functional, integrated, and verified.

```bash
git tag -a v5.0.0 -m "Phases 1-5 Complete"
git push origin v5.0.0
```

---

## license

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=2d1f5e,7c5cbf,b39ddb&height=100&section=footer" />

*Built by [Samiksha Patil](https://github.com/sammmiksha) — Mumbai, India*

</div>
