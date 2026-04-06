# Itinera — AI Activity Planner

> A multi-agent AI system that plans real-world activities, outings, and experiences using Google ADK, Gemini 2.5 Flash, and MCP Toolbox.

## Live Demo
**🌐 Frontend:** https://itinera-frontend-662889849418.us-central1.run.app

---

## What It Does

Tell Itinera what you want — *"Plan a romantic dinner in Bandra, Mumbai, budget ₹3000 for two"* — and it returns a complete, timed itinerary with real venues, walking/transit directions, cost estimates, and score badges.

---

## Architecture

```
User → React Frontend
         ↓
    FastAPI Backend (Cloud Run)
         ↓
    ADK Orchestrator Agent
    ├── Scout Agent       → Google Places API (real venues)
    ├── Transit Agent     → Google Routes API (transport legs)
    └── Planner Agent     → Builds timed itinerary
         ↓
    MCP Toolbox (Cloud Run)
         ↓
    Neon PostgreSQL (save/retrieve plans)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Agents | Google Agent Development Kit (ADK) |
| LLM | Gemini 2.5 Flash via Vertex AI |
| Places | Google Places API (New) |
| Routes | Google Routes API |
| MCP | MCP Toolbox for Databases |
| Database | Neon PostgreSQL (production: AlloyDB) |
| Backend | FastAPI + Python 3.11 |
| Frontend | React + Vite |
| Deployment | Google Cloud Run (3 services) |
| Registry | Google Artifact Registry |
| Build | Google Cloud Build |

---

## Services

| Service | URL |
|---|---|
| Frontend | https://itinera-frontend-662889849418.us-central1.run.app |
| Backend API | https://itinera-backend-662889849418.us-central1.run.app |
| MCP Toolbox | https://itinera-toolbox-662889849418.us-central1.run.app |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/query` | Generate an itinerary |
| POST | `/calendar` | Save itinerary to calendar |
| GET | `/plans/{user_id}` | Retrieve past plans |

### Example Query
```bash
curl -X POST https://itinera-backend-662889849418.us-central1.run.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Plan a lunch date at Connaught Place, Delhi. Casual vibe, budget 2000 rupees for two.",
    "user_id": "demo_user"
  }'
```

---

## Agent Architecture

- **Orchestrator** — Primary ADK agent. Parses user intent, coordinates all sub-agents, returns final itinerary JSON.
- **Scout Agent** — Finds real venues using Google Places API based on location, vibe, and budget.
- **Transit Agent** — Calculates transport between stops using Google Routes API.
- **Planner Agent** — Assembles timed itinerary with cost estimates and scores.

---

## MCP Toolbox Tools

| Tool | Description |
|---|---|
| `save-plan` | Saves a completed itinerary to PostgreSQL |
| `get-past-plans` | Retrieves past plans for a user |
| `get-user-preferences` | Fetches stored user preferences |
| `save-user-preferences` | Saves/updates user preferences |

---

## Project Structure

```
Itinera/
├── backend/
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── scout_agent.py
│   │   ├── transit_agent.py
│   │   └── planner_agent.py
│   ├── tools/
│   │   ├── places_tool.py
│   │   ├── routes_tool.py
│   │   ├── memory_tools.py
│   │   └── calendar_tool.py
│   ├── models/
│   │   └── intent.py
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatPanel.jsx
│   │   │   └── ItineraryPanel.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   └── nginx.conf
├── toolbox/
│   ├── tools.yaml
│   └── Dockerfile
├── cloudbuild.yaml
├── cloudbuild-frontend.yaml
└── cloudbuild-toolbox.yaml
```

---

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- Google Cloud SDK
- GCP project with Vertex AI enabled

### Backend
```bash
cd Itinera
pip install -r backend/requirements.txt

export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=true
export GEMINI_MODEL=gemini-2.5-flash
export GOOGLE_MAPS_API_KEY=your-maps-api-key
export PYTHONPATH=.

uvicorn backend.main:app --host 0.0.0.0 --port 8080
```

### Frontend
```bash
cd frontend
echo "VITE_BACKEND_URL=http://localhost:8080" > .env
npm install
npm run dev
```

---

## Built With

- [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
- [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/)
- [MCP Toolbox for Databases](https://googleapis.github.io/genai-toolbox/)
- [Google Cloud Run](https://cloud.google.com/run)
- [Neon PostgreSQL](https://neon.tech)
- [React](https://react.dev) + [Vite](https://vitejs.dev)
