import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .agent_runner import run_agent_with_logs
from .schemas import QueryRequest, QueryResponse


app = FastAPI(title="human-in-the-loop API")


origins = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(",")
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.post("/query", response_model=QueryResponse)
async def query_agent(payload: QueryRequest):
try:
answer, used_tool, logs = run_agent_with_logs(payload.query)
return QueryResponse(answer=answer, used_tool=used_tool, logs=logs)
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))