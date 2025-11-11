# AI Productivity Coach — MVP


This repo contains a minimal AI Productivity Coach with a React frontend and FastAPI backend. The backend exposes `/api/chat` that forwards messages to OpenAI (or any LLM) and saves sessions to SQLite.


## Quick start


### Backend
1. cd backend
2. python -m venv .venv
3. source .venv/bin/activate # or .\.venv\Scripts\activate on Windows
4. pip install -r requirements.txt
5. create a `.env` from `.env.example` and set OPENAI_API_KEY
6. uvicorn app.main:app --reload --port 8000


### Frontend
1. cd frontend
2. npm install
3. npm run dev


Open http://localhost:5173 (frontend) and http://localhost:8000/docs (FastAPI docs)