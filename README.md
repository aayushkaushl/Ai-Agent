# AI Agent

Welcome to **Human-in-the-Loop AI Agent**, a production-ready AI assistant platform that allows you to:

* Search the internet for current events and general information.
* Query Wikipedia for factual information.
* Execute Python code for calculations or data analysis.

This project is designed with a clean separation of **frontend** (Streamlit) and **backend** (FastAPI) for scalability, maintainability, and production deployment.

---

## Project Structure

```
Ai-Agent/
├─ backend/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py                # FastAPI app exposing /query endpoint
│  │  ├─ agent_runner.py        # Handles AI agent initialization and execution
│  │  └─ schemas.py             # Pydantic models for requests/responses
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ .env.example
├─ frontend/
│  ├─ streamlit_app.py         # Streamlit frontend UI that interacts with backend
│  ├─ requirements.txt
│  └─ .env.example
├─ docker-compose.yml
├─ .gitignore
├─ README.md
└─ LICENSE
```

---

## Features

1. **AI-Powered Agent**: Integrates Google Generative AI (`gemini-1.5-flash`) for natural language understanding.
2. **Google Search Tool**: Retrieves current web information using Serper API.
3. **Wikipedia Tool**: Provides factual data from Wikipedia.
4. **Python REPL Tool**: Executes Python code for calculations, data analysis, or simulations.
5. **Conversation Memory**: Maintains context between queries for more intelligent responses.
6. **Extensible Architecture**: Easily add more tools or change LLM without rewriting the codebase.

---

## Getting Started

### Prerequisites

* Python 3.11+
* Git
* (Optional) Docker & Docker Compose

### Setup Instructions

1. **Clone Repository**

```bash
git clone <your-repo-url> Ai-Agent
cd Ai-Agent
```

2. **Backend Setup**

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows
# or source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
cp .env.example .env            # Fill your API keys
uvicorn app.main:app --reload --port 8000
```

3. **Frontend Setup**

```bash
cd ../frontend
python -m venv .venv
source .venv/Scripts/activate   # Windows
# or source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
cp .env.example .env            # Set BACKEND_URL=http://localhost:8000/query
streamlit run streamlit_app.py --server.port 8501
```

### Docker Setup (Optional)

```bash
docker-compose up --build
```

* Frontend: [http://localhost:8501](http://localhost:8501)
* Backend: [http://localhost:8000/query](http://localhost:8000/query)

---

## Environment Variables

### Backend (.env)

```
OPENAI_API_KEY=
GOOGLE_API_KEY=
GOOGLE_MODEL=gemini-1.5-flash
TEMPERATURE=0
MAX_ITERATIONS=2
CORS_ORIGINS=http://localhost:8501
```

### Frontend (.env)

```
BACKEND_URL=http://localhost:8000/query
```

> **Important:** Never commit `.env` files with real API keys.

---

## How it Works

1. User submits a query through the Streamlit frontend.
2. Frontend sends query to FastAPI backend.
3. Backend invokes the AI agent with memory context and all available tools.
4. The agent decides which tool to use (Google, Wikipedia, Python REPL) and executes the action.
5. Response, logs, and last used tool info are returned to frontend.
6. Conversation memory is updated for context-aware replies.

---

## Contributing

* Fork the repository
* Create a feature branch
* Commit your changes
* Open a pull request

---

## License

© 2025 Aayush Kaushal. All rights reserved.

---

## Notes

* Rotate your API keys regularly.
* Use `.env.example` for safe sharing.
* Extend the agent by adding new `Tool` instances in `agent_runner.py`.
* This project is ready for production deployment with Docker or any cloud service.
